"""Memorization tools: commutator library, HTR subset naming, subset finishes.

Things a strong human FMC solver has memorized. The agent gets them as
lookups so it doesn't need to derive them from first principles.
"""

from __future__ import annotations

from cube.analyzer.insertions import COMMUTATORS, analyze_residual
from cube.classifier.features import Axis
from cube.classifier.htr import (
    dr_subset_canonical,
    htr_corner_perms,
    is_htr,
    is_htr_ud,
)
from cube.engine.notation import parse_alg
from cube.engine.state import SOLVED


def _state_after(scramble: list[str], history: list[str]):
    s = SOLVED.apply_alg(parse_alg(" ".join(scramble))) if scramble else SOLVED
    if history:
        s = s.apply_alg(parse_alg(" ".join(history)))
    return s


def lookup_commutator(cycle_type: str | None = None) -> dict:
    """Return the agent's commutator library, optionally filtered by cycle type.

    `cycle_type` (optional): one of `corner_3cycle`, `edge_3cycle`,
      `corner_twist_2`, `edge_flip_2`, or `None` for the full library.

    Each entry has `name`, `moves` (WCA notation list), `length`,
    `cycle_type`, and `signature` (the cycle the commutator performs when
    applied to SOLVED, in slot-index form).

    A human solver has internalized ~5-20 commutators; the library size
    here (~16 entries) is comparable.
    """
    entries = []
    for c in COMMUTATORS:
        if cycle_type is not None and c.cycle_type != cycle_type:
            continue
        entries.append({
            "name": c.name,
            "moves": [str(m) for m in c.moves],
            "length": len(c),
            "cycle_type": c.cycle_type,
            "signature": [list(cyc) for cyc in c.signature],
            "affected_slots": list(c.affected_slots),
        })
    return {
        "library_size": len(COMMUTATORS),
        "matching": len(entries),
        "entries": entries,
    }


def htr_subset(scramble: list[str], history: list[str]) -> dict:
    """Identify the HTR corner subset of the current state, if in HTR.

    Strong FMC solvers recognize HTR subsets by name (e.g. "4c1", "2c3").
    Each subset has a known approximate optimal finish length; that's how
    a human knows "this subset is easy / hard."

    Returns:
      - `in_canonical_htr_ud`: bool — is the state in is_htr_ud at all
      - `in_strict_htr`: bool — is it in the multi-axis strict HTR
      - `corner_subset_canonical`: the canonical-form cp tuple, if in
        DR-corner subgroup. Hashable so the agent can compare across states.
      - `note`: explanation
    """
    s = _state_after(scramble, history)
    canonical = dr_subset_canonical(s)
    return {
        "in_canonical_htr_ud": bool(is_htr_ud(s)),
        "in_strict_htr": bool(is_htr(s)),
        "corner_subset_canonical": list(canonical) if canonical is not None else None,
        "note": (
            "HTR-corner subsets are 420 distinct cosets of the 96-element "
            "HTR-corner subgroup inside the 40320-element DR-corner set. "
            "States with the same canonical form have similar finish difficulty."
        ),
    }


def residual_cycles(scramble: list[str], history: list[str]) -> dict:
    """Classify what's left to solve after the given moves.

    Useful for the agent to know "the state has a 3-cycle of corners, so
    look up corner_3cycle commutators." Returns the cycle structure plus
    a recommended cycle type for `lookup_commutator`.
    """
    s = _state_after(scramble, history)
    r = analyze_residual(s)
    return {
        "is_solved": r.is_solved,
        "cycle_type": r.cycle_type,
        "corner_perm_cycles": [list(cyc) for cyc in r.corner_perm_cycles],
        "edge_perm_cycles": [list(cyc) for cyc in r.edge_perm_cycles],
        "corner_twist_slots": [list(x) for x in r.corner_twists],
        "edge_flip_slots": [list(x) for x in r.edge_flips],
        "recommended_lookup_type": (
            r.cycle_type if r.cycle_type in {
                "corner_3cycle", "edge_3cycle",
                "corner_twist_2", "edge_flip_2",
            } else None
        ),
    }
