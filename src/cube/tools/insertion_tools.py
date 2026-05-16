"""Human-shaped insertion tools.

These are NOT search. Each tool does O(1) lookups or single-pass observations:

- analyze_current_residual: classify the current cube's residual (3c, 3c3c,
  2e2e, mixed, etc.) so the agent can SEE what's left to solve.
- derive_corner_3cycle: if the residual IS a pure corner 3-cycle, return
  the canonical commutator from the pre-built table. Closed-form lookup.
- replace_and_shorten: take a sub-span of the agent's current history,
  apply it as a fresh micro-scramble, run the existing DR/HTR pipeline
  on the micro-state, and return a (possibly) shorter substitute.
  Recursive reuse of existing tools — NOT new search.

Grounded in Sebastiano Tronto, Fewest Moves Tutorial v3.04:
- §2.3, §2.4.1: 3-cycle commutator derivation
- §3.10: "Replace and shorten"
"""

from __future__ import annotations

from cube.analyzer.commutator_table import (
    _canonicalize_cycle,
    _extract_corner_residual_key,
    _extract_pure_3cycle_corners,
    _extract_pure_3cycle_edges,
    lookup_corner_3cycle,
    lookup_edge_3cycle,
)
from cube.analyzer.insertions import analyze_residual
from cube.engine.notation import parse_alg
from cube.engine.state import SOLVED, State, EDGE_NAMES, CORNER_NAMES


def _current_state(scramble: list[str], history: list[str]) -> State:
    s = SOLVED.apply_alg(parse_alg(" ".join(scramble))) if scramble else SOLVED
    if history:
        s = s.apply_alg(parse_alg(" ".join(history)))
    return s


def analyze_current_residual(scramble: list[str], history: list[str]) -> dict:
    """Classify the current cube's residual — what's left to solve.

    Returns a dict with:
      - residual_class: 'solved', 'corner_3cycle', 'edge_3cycle', 'mixed', etc.
      - corner_perm_cycles: list of slot cycles (as name tuples)
      - edge_perm_cycles: list of slot cycles
      - corner_twists: [(slot_name, twist), ...]
      - edge_flips: [(slot_name, 1), ...]
      - is_solved: bool
      - is_pure_corner_3cycle: bool — if True, derive_corner_3cycle can fix it
      - num_unsolved_pieces: count

    Use this AT ANY POINT during the solve to see if you've landed on an
    insertable residual. Cheap; same shape as inspect_state.
    """
    state = _current_state(scramble, history)
    residual = analyze_residual(state)

    def _cycle_names(cycles, name_list):
        return [
            [name_list[i] for i in cycle] for cycle in cycles
        ]

    def _named_orient(pairs, name_list):
        return [(name_list[i], v) for i, v in pairs]

    pure_corner_3c = bool(_extract_pure_3cycle_corners(state))
    pure_edge_3c = bool(_extract_pure_3cycle_edges(state))

    # Count unsolved pieces (any corner not home-and-oriented, any edge same).
    n_corners_unsolved = sum(
        1 for i in range(8)
        if state.cp[i] != i or state.co[i] != 0
    )
    n_edges_unsolved = sum(
        1 for i in range(12)
        if state.ep[i] != i or state.eo[i] != 0
    )

    return {
        "residual_class": residual.cycle_type,
        "corner_perm_cycles": _cycle_names(residual.corner_perm_cycles, CORNER_NAMES),
        "edge_perm_cycles": _cycle_names(residual.edge_perm_cycles, EDGE_NAMES),
        "corner_twists": _named_orient(residual.corner_twists, CORNER_NAMES),
        "edge_flips": _named_orient(residual.edge_flips, EDGE_NAMES),
        "is_solved": residual.is_solved,
        "is_pure_corner_3cycle": pure_corner_3c,
        "is_pure_edge_3cycle": pure_edge_3c,
        "num_corners_unsolved": n_corners_unsolved,
        "num_edges_unsolved": n_edges_unsolved,
        "num_pieces_unsolved": n_corners_unsolved + n_edges_unsolved,
    }


def derive_corner_3cycle(scramble: list[str], history: list[str]) -> dict:
    """If the current state is a pure corner 3-cycle, return the canonical
    8-move commutator that performs that exact cycle.

    Closed-form lookup from the precomputed table (112 corner cycles
    covered, all reachable pure 3-cycles). Returns the commutator move
    sequence in WCA notation. Apply it with apply_moves to complete the
    solve.

    Returns:
      - if pure corner 3-cycle: {found: 1, cycle: [...names...],
        moves: [...], length: 8, note: '8-move corner 3-cycle commutator'}
      - else: {found: 0, note: 'state is not a pure corner 3-cycle'}
    """
    state = _current_state(scramble, history)
    key = _extract_corner_residual_key(state)
    if key is None:
        return {
            "found": 0,
            "note": "Current state is not a pure corner 3-cycle. "
                    "Run analyze_current_residual to see what's left."
        }
    a, b, c, ta, tb, tc = key
    # To UNDO this residual, we need the comm that produces the INVERSE
    # residual: inverse cycle (a, c, b) with twists determined by the
    # inverse cube state. Twists are constrained by sum=0 mod 3. Try all
    # 9 valid (t1, t2, t3) combinations for (a, c, b) and verify by applying.
    cycle_named = [CORNER_NAMES[i] for i in (a, b, c)]
    for t1 in range(3):
        for t2 in range(3):
            t3 = (-t1 - t2) % 3
            candidate_key = (a, c, b, t1, t2, t3)
            moves = lookup_corner_3cycle(candidate_key)
            if moves is None:
                continue
            # Verify by applying.
            new_state = state.apply_alg(parse_alg(" ".join(moves)))
            if new_state == SOLVED:
                return {
                    "found": 1,
                    "cycle": cycle_named,
                    "moves": list(moves),
                    "length": len(moves),
                    "note": (
                        f"Derived 8-move corner 3-cycle commutator for "
                        f"{cycle_named} — apply with apply_moves to solve."
                    ),
                }
    return {
        "found": 0,
        "cycle": cycle_named,
        "note": "Pure corner 3-cycle detected but no matching commutator "
                "found in the table. Should not happen for any reachable "
                "(cycle + twist) residual.",
    }


def _try_solve_micro_scramble(micro_moves: list[str], axis: str = "UD") -> dict:
    """Apply micro_moves to SOLVED as a fresh scramble, then run the
    existing EO + DR + HTR pipeline to solve it. Returns the best
    short solve found, or empty if pipeline fails.
    """
    from cube.tools.eo_pattern_lib import eo_pattern_lookup
    from cube.tools.dr_pattern_lib import dr_pattern_lookup
    from cube.tools import search as tsearch

    sc = list(micro_moves)
    hist: list[str] = []
    eo = eo_pattern_lookup(sc, hist, axis=axis)
    if eo.get("found") != 1:
        return {"solved": False, "reason": "no EO found"}
    eo_moves = eo["options"][0]["moves"]
    hist = list(eo_moves)
    dr = dr_pattern_lookup(sc, hist, axis=axis)
    if dr.get("found") != 1:
        return {"solved": False, "reason": "no DR found"}
    dr_moves = dr["options"][0]["moves"]
    hist += list(dr_moves)
    # Now run htr_and_finish.
    full = tsearch.solve_htr_and_finish_from_dr(sc, hist, axis=axis)
    if "error" in full:
        return {"solved": False, "reason": "htr/finish failed"}
    finish_moves = list(full["htr_moves"]) + list(full["finish_moves"])
    full_solution = eo_moves + dr_moves + finish_moves
    return {
        "solved": True,
        "moves": full_solution,
        "length": len(full_solution),
    }


def replace_and_shorten(
    scramble: list[str], history: list[str],
    start: int, end: int,
    axis: str = "UD",
) -> dict:
    """Tronto §3.10 — "Replace and shorten."

    Take history[start:end] (a "suspicious" sub-sequence), apply it to a
    solved cube as a fresh micro-scramble, run the existing DR/HTR
    pipeline to solve that micro-state, and return the shorter substitute
    (if any) along with the resulting full history.

    This is RECURSIVE REUSE of existing tools, not a new search.

    Returns:
      - {original_len, substitute_len, delta, original, substitute,
        new_history, full_history_len, solves_scramble: bool}
    """
    span = list(history[start:end])
    if not span:
        return {"error": f"empty span [{start}:{end}]"}
    original_len = len(span)

    micro = _try_solve_micro_scramble(span, axis=axis)
    if not micro.get("solved"):
        return {
            "error": f"could not solve micro-scramble for span [{start}:{end}]: "
                     f"{micro.get('reason')}"
        }

    # The micro-scramble was applied as `span` to SOLVED. To solve it via
    # `substitute`, we need substitute = inverse(span_solution) such that
    # span * substitute = identity? Actually no: micro["moves"] applied
    # AFTER span solves it, so substitute_for_span = micro["moves"] applied
    # AFTER the original span doesn't work as a REPLACEMENT for span.
    #
    # The replace-and-shorten trick: span produces some state. We want a
    # SHORTER sequence with the SAME effect as span. From SOLVED+span, the
    # solver finds moves to reach SOLVED. Therefore span ≡ inverse(solver)
    # (since span * solver = identity). So the substitute = inverse(solver).
    inverse_solver = list(reversed([
        # Invert each move string
        _invert_move_str(m) for m in micro["moves"]
    ]))
    substitute = inverse_solver
    new_history = list(history[:start]) + substitute + list(history[end:])

    # Verify the full new history still solves the original scramble.
    full_state = _current_state(scramble, new_history)
    solves = full_state == SOLVED

    return {
        "span_range": [start, end],
        "original": span,
        "substitute": substitute,
        "original_len": original_len,
        "substitute_len": len(substitute),
        "delta": len(substitute) - original_len,
        "new_history_len": len(new_history),
        "new_history": new_history,
        "solves_scramble": solves,
        "note": (
            f"Span [{start}:{end}] ({original_len} moves) -> substitute "
            f"({len(substitute)} moves). "
            f"Delta {len(substitute) - original_len:+d}. "
            f"{'SOLVES' if solves else 'DOES NOT SOLVE'} original scramble."
        ),
    }


def _invert_move_str(m: str) -> str:
    """Invert a move in WCA notation: R -> R', R' -> R, R2 -> R2."""
    if m.endswith("'"):
        return m[:-1]
    if m.endswith("2"):
        return m
    return m + "'"
