"""Algebraic tools: cancellation, NISS frame switching.

Both are mechanical operations a human FMC solver performs on paper. The
agent gets them as pure functions so it doesn't have to track them manually.
"""

from __future__ import annotations

from cube.engine.cancellation import cancel_moves
from cube.engine.notation import invert_alg, parse_alg


def cancel(moves: list[str]) -> dict:
    """Apply local cancellation rules to a move sequence.

    Handles same-face combine (e.g. `U U' -> nothing`, `U U2 -> U'`) and
    through-commute (e.g. `U D U -> D U2`). Returns the cancelled sequence
    and the savings count.
    """
    parsed = parse_alg(" ".join(moves)) if moves else []
    cancelled = cancel_moves(parsed)
    cancelled_str = [str(m) for m in cancelled]
    return {
        "input_length": len(parsed),
        "cancelled_length": len(cancelled),
        "saved": len(parsed) - len(cancelled),
        "cancelled_moves": cancelled_str,
    }


def niss_flip(scramble: list[str], history: list[str]) -> dict:
    """Switch from the normal frame to the inverse frame (NISS).

    Given a scramble and a sequence of moves played on it, return the
    equivalent move list as if the solver had been working on the inverse
    scramble from the start. The new sequence solves the *inverse*
    scramble back to its current state.

    Concretely: under NISS, applying inverse-side moves `I` is equivalent
    to applying `invert(I)` as premoves on the normal scramble. This tool
    gives the agent the inverse-frame history representation so it can
    continue search there.

    Returns:
      - `inverse_scramble`: the inverted scramble (as moves)
      - `inverse_history`: history reinterpreted on the inverse side
    """
    inv_scramble = [str(m) for m in invert_alg(parse_alg(" ".join(scramble)))]
    # In the inverse frame, the cumulative state is `invert(scramble + history)`
    # applied to SOLVED. So the equivalent "history on the inverse side"
    # is the empty list -- the inverse-scramble *itself* (= invert(scramble + history))
    # encodes everything. Practically, give the agent both forms.
    cumulative = parse_alg(" ".join(scramble + history))
    inv_cumulative = invert_alg(cumulative)
    return {
        "original_scramble": scramble,
        "original_history": history,
        "inverse_scramble": inv_scramble,
        "inverse_cumulative": [str(m) for m in inv_cumulative],
        "note": (
            "To continue search on the inverse side, treat "
            "`inverse_cumulative` as the new effective scramble applied to "
            "SOLVED, and run search from there. Moves you find on this side "
            "are 'inverse-side' moves; the final solution is "
            "`normal_moves + invert(inverse_moves)` applied to the "
            "original scramble."
        ),
    }


def invert(moves: list[str]) -> dict:
    """Invert a move sequence. (Mechanical.)"""
    inverted = invert_alg(parse_alg(" ".join(moves))) if moves else []
    return {"inverted": [str(m) for m in inverted]}
