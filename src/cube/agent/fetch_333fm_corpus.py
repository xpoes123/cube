"""Fetch a small corpus of WCA-FMC scrambles + human reconstructions from api.333.fm.

Output: a JSON file with N entries, each containing:
  - id: stable identifier ("comp_<wcaCompetitionId>_s<number>")
  - scramble: scramble string
  - human_solution: the human's final move string (post-insertions)
  - human_moves: WCA move count from the API (centimoves/100)
  - human_comment: free-text phase annotations (EO/DR/HTR/etc.)
  - solver: name/wcaId of the human
  - competition: comp ID

The corpus_eval.py loader prefers this file when present, so the same
scrambles are used by every corpus run.

Usage:
    uv run python -m cube.agent.fetch_333fm_corpus --n 5
"""

from __future__ import annotations

import argparse
import json
import time
import urllib.request
from pathlib import Path

API_BASE = "https://api.333.fm"
DEFAULT_OUT = Path("data/corpus_333fm.json")


def _get(path: str) -> dict:
    url = f"{API_BASE}{path}"
    with urllib.request.urlopen(url, timeout=15) as r:
        return json.loads(r.read())


def fetch_corpus(n: int, page: int = 1) -> list[dict]:
    """Walk comps -> users -> submissions until we have `n` unique scrambles.

    Skips inverse submissions and submissions without a clean solution+comment.
    """
    out: list[dict] = []
    seen_scrambles: set[str] = set()
    current_page = page
    while len(out) < n:
        comps = _get(f"/wca/reconstruction?page={current_page}")
        items = comps.get("items") or []
        if not items:
            break
        for comp_row in items:
            wca_id = comp_row["wcaCompetitionId"]
            if len(out) >= n:
                break
            try:
                detail = _get(f"/wca/reconstruction/{wca_id}")
            except Exception as e:
                print(f"  skip {wca_id} (detail): {e}")
                continue
            for recon in detail.get("recons", []):
                user_id = recon["userId"]
                if len(out) >= n:
                    break
                try:
                    sub_data = _get(
                        f"/wca/reconstruction/{wca_id}/user/{user_id}"
                    )
                except Exception as e:
                    print(f"  skip {wca_id}/{user_id}: {e}")
                    continue
                for sub in sub_data.get("submissions", []):
                    if sub.get("inverse"):
                        continue
                    if not sub.get("solution"):
                        continue
                    scramble = (sub.get("scramble") or {}).get("scramble")
                    if not scramble or scramble in seen_scrambles:
                        continue
                    moves = sub.get("wcaMoves") or sub.get("moves") or 0
                    out.append({
                        "id": f"fm_{wca_id}_s{sub['scramble']['number']}",
                        "scramble": scramble,
                        "human_solution": sub["solution"],
                        "human_moves": moves // 100,
                        "human_comment": sub.get("comment") or "",
                        "solver": recon["user"]["name"],
                        "solver_wca_id": recon["user"].get("wcaId"),
                        "competition": wca_id,
                    })
                    seen_scrambles.add(scramble)
                    if len(out) >= n:
                        break
                time.sleep(0.3)  # polite to the API
            time.sleep(0.3)
        current_page += 1
        if current_page > 10:
            break
    return out


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--n", type=int, default=5)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--page", type=int, default=1)
    args = parser.parse_args()

    print(f"Fetching {args.n} scrambles from {API_BASE} ...")
    corpus = fetch_corpus(args.n, page=args.page)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(corpus, indent=2))
    print(f"\nWrote {len(corpus)} entries to {args.out}")
    for c in corpus:
        print(f"  {c['id']}: {c['human_moves']} moves by {c['solver']}")


if __name__ == "__main__":
    main()
