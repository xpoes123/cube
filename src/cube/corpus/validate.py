"""Validate reconstructions against the cube engine.

A reconstruction is valid iff applying its scramble + solution to SOLVED
returns to SOLVED. Any record that fails validation is quarantined — it
indicates either a parse bug, a typo in the source, or a notation we don't
yet handle (slice moves, wide moves, rotations). Quarantined records are
saved for inspection but excluded from training data.
"""

from __future__ import annotations

from dataclasses import dataclass

from cube.corpus.types import Reconstruction
from cube.engine.state import SOLVED


@dataclass(frozen=True, slots=True)
class ValidationResult:
    ok: bool
    reason: str | None = None

    def __bool__(self) -> bool:
        return self.ok


def validate(rec: Reconstruction) -> ValidationResult:
    """Check scramble + solution returns to SOLVED."""
    try:
        scrambled = SOLVED.apply_alg(rec.scramble)
        final = scrambled.apply_alg(rec.solution.flat())
    except (KeyError, IndexError, ValueError) as e:
        return ValidationResult(ok=False, reason=f"engine error: {e}")
    if final != SOLVED:
        # Useful diagnostic: how far off?
        bad_corners = sum(1 for i in range(8) if final.cp[i] != i or final.co[i] != 0)
        bad_edges = sum(1 for i in range(12) if final.ep[i] != i or final.eo[i] != 0)
        return ValidationResult(
            ok=False,
            reason=f"unsolved: {bad_corners} bad corners, {bad_edges} bad edges",
        )
    return ValidationResult(ok=True)
