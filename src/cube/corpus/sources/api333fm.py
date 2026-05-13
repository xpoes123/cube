"""333.fm API client and adapter to Reconstruction.

See `memory/reference_333fm_api.md` for endpoint walk.

Submission → Reconstruction mapping:
- `scramble.scramble`     → Reconstruction.scramble
- `solution`              → Reconstruction.solution (parsed as NISS, usually no parens
                             since the solution field is post-insertions)
- `comment`               → Reconstruction.commentary (rich phase-annotated text;
                             we don't parse it here — the segmenter handles that)
- nested user, competition → author / competition metadata
- `inverse: true` submissions are skipped in v1 (semantics need verification)
"""

from __future__ import annotations

import hashlib
import json
import time
from collections.abc import Iterator
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any

import httpx

from cube.corpus.types import Reconstruction
from cube.engine.notation import parse_alg, parse_niss

BASE_URL = "https://api.333.fm"
SOURCE_NAME = "333.fm"
DEFAULT_DELAY_SEC = 0.5
DEFAULT_TIMEOUT_SEC = 30.0
USER_AGENT = "cube-research/0.0 (FMC analysis project)"


@dataclass(slots=True)
class FetchStats:
    requests: int = 0
    cache_hits: int = 0
    parse_failures: int = 0
    inverse_skipped: int = 0


class Api333fmClient:
    """Minimal client: GETs, polite rate limit, optional on-disk JSON cache."""

    def __init__(
        self,
        base_url: str = BASE_URL,
        delay_sec: float = DEFAULT_DELAY_SEC,
        cache_dir: str | Path | None = None,
        timeout_sec: float = DEFAULT_TIMEOUT_SEC,
    ):
        self.base_url = base_url.rstrip("/")
        self.delay_sec = delay_sec
        self.cache_dir = Path(cache_dir) if cache_dir else None
        self._client = httpx.Client(
            timeout=timeout_sec,
            headers={"User-Agent": USER_AGENT, "Accept": "application/json"},
        )
        self._last_request_at = 0.0
        self.stats = FetchStats()

    def get(self, path: str) -> dict[str, Any]:
        if self.cache_dir is not None:
            cache_path = self._cache_path(path)
            if cache_path.exists():
                self.stats.cache_hits += 1
                return json.loads(cache_path.read_text())

        # Polite rate limit.
        wait = self.delay_sec - (time.monotonic() - self._last_request_at)
        if wait > 0:
            time.sleep(wait)

        resp = self._client.get(f"{self.base_url}{path}")
        self._last_request_at = time.monotonic()
        self.stats.requests += 1
        resp.raise_for_status()
        data = resp.json()

        if self.cache_dir is not None:
            cache_path = self._cache_path(path)
            cache_path.parent.mkdir(parents=True, exist_ok=True)
            cache_path.write_text(json.dumps(data))
        return data

    def _cache_path(self, path: str) -> Path:
        assert self.cache_dir is not None
        h = hashlib.sha1(path.encode("utf-8")).hexdigest()[:16]
        return self.cache_dir / f"{h}.json"

    # --- High-level traversal ---

    def iter_wca_competitions(self) -> Iterator[dict[str, Any]]:
        page = 1
        while True:
            data = self.get(f"/wca/reconstruction?page={page}")
            yield from data.get("items", [])
            meta = data.get("meta", {})
            if page >= meta.get("totalPages", page):
                return
            page += 1

    def get_competition(self, wca_competition_id: str) -> dict[str, Any]:
        return self.get(f"/wca/reconstruction/{wca_competition_id}")

    def get_user_submissions(self, wca_competition_id: str, user_id: int) -> dict[str, Any]:
        return self.get(f"/wca/reconstruction/{wca_competition_id}/user/{user_id}")

    def close(self) -> None:
        self._client.close()


def submission_to_reconstruction(
    submission: dict[str, Any],
    *,
    recon: dict[str, Any],
    competition_name: str,
    stats: FetchStats | None = None,
) -> Reconstruction | None:
    """Map a 333.fm submission record to a Reconstruction.

    Returns None for records we can't ingest (parse failure, inverse-form, empty).
    Increments `stats` counters when supplied.
    """
    solution_str = submission.get("solution")
    if not solution_str:
        return None

    if submission.get("inverse"):
        if stats is not None:
            stats.inverse_skipped += 1
        return None

    scramble_obj = submission.get("scramble") or {}
    scramble_str = scramble_obj.get("scramble")
    if not scramble_str:
        return None

    try:
        scramble = parse_alg(scramble_str)
        solution = parse_niss(solution_str)
    except ValueError:
        if stats is not None:
            stats.parse_failures += 1
        return None

    user = recon.get("user", {})
    created_at = submission.get("createdAt")
    date_solved = None
    if created_at:
        try:
            date_solved = datetime.fromisoformat(created_at.replace("Z", "+00:00")).date()
        except ValueError:
            pass

    sub_id = submission.get("id")
    comp_id = submission.get("competitionId")
    user_id = submission.get("userId")
    return Reconstruction(
        scramble=scramble,
        solution=solution,
        source=SOURCE_NAME,
        source_id=f"wca:{comp_id}:{user_id}:{sub_id}",
        author=user.get("name") or user.get("wcaId"),
        competition=competition_name,
        commentary=submission.get("comment") or None,
        date_solved=date_solved,
    )


def iter_wca_reconstructions(client: Api333fmClient) -> Iterator[Reconstruction]:
    """Walk competitions → recon records → submissions, yielding Reconstructions."""
    for comp_summary in client.iter_wca_competitions():
        wca_id = comp_summary.get("wcaCompetitionId")
        if not wca_id:
            continue
        try:
            comp_data = client.get_competition(wca_id)
        except httpx.HTTPError:
            continue
        comp_name = comp_data.get("competition", {}).get("name") or wca_id
        for recon in comp_data.get("recons", []):
            user_id = recon.get("userId")
            if user_id is None:
                continue
            try:
                user_data = client.get_user_submissions(wca_id, user_id)
            except httpx.HTTPError:
                continue
            recon_full = user_data.get("recon", recon)
            for sub in user_data.get("submissions", []):
                rec = submission_to_reconstruction(
                    sub, recon=recon_full, competition_name=comp_name, stats=client.stats
                )
                if rec is not None:
                    yield rec
