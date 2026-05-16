"""Greedy skeleton finder — maximize-solved-pieces hill climb.

This is the human-shaped "naturally produce a skeleton" tool: from
post-DR (or post-EO), apply a greedy beam-search that picks moves
maximizing the count of home-and-oriented pieces. Track every state
along the way whose residual is INSERTABLE per Tronto §2.4 — 3c, 3c1t,
2e2e, 5c, 3c3c, etc. — and discard skeletons whose residual is too
complex to finish in ≤2 commutators (4c1t, 3c2t, 4t, 5t, mixed).

Per Sebastiano Tronto, Fewest Moves Tutorial §2.4 (residual classes):
  WORTH PURSUING: 3c, 3s1t, 2s2s, 5s, 3s3s, 2t, 3t, edge 3-cycles
  DISCARD: 4c1t, 3c2t, 4t, 5t, complex, or anything needing 3+ comms

NOT A* — this is greedy hill-climb with small beam, the same gradient-
following move-selection a human does when block-building.
"""

from __future__ import annotations

from cube.analyzer.insertions import analyze_residual
from cube.classifier.features import Axis, is_dr, is_eo_solved
from cube.engine.moves import Face, Move, Turn
from cube.engine.notation import parse_alg
from cube.engine.state import SOLVED, State


# Per Tronto §2.4: residual classes solvable in ≤2 commutators.
_WORTH_PURSUING_CLASSES = frozenset({
    "solved",
    "corner_3cycle",
    "edge_3cycle",
    "corner_3c1t",
    "edge_2e2e",
    "corner_3c3c",
    "corner_5cycle",
    "edge_3c3c",
    "edge_5cycle",
    "corner_twist_2",
    "edge_flip_2",
})


# Move sets per phase. Post-DR: stay in DR group <U, D, R2, L2, F2, B2>
# (keeps EO, CO, slice intact). Post-EO: stay in EO-preserving group.
def _dr_group_moves(axis: Axis) -> tuple[Move, ...]:
    if axis == Axis.UD:
        flipping = (Face.F, Face.B)
    elif axis == Axis.FB:
        flipping = (Face.L, Face.R)
    else:
        flipping = (Face.U, Face.D)
    return tuple(
        Move(f, t) for f in Face for t in Turn
        if not (f in flipping and t != Turn.HALF)
    )


def _count_solved_pieces(state: State) -> int:
    """Number of pieces home AND oriented."""
    n = 0
    for i in range(8):
        if state.cp[i] == i and state.co[i] == 0:
            n += 1
    for i in range(12):
        if state.ep[i] == i and state.eo[i] == 0:
            n += 1
    return n


def _greedy_score(state: State) -> float:
    """Score for greedy beam: solved-piece count plus bonus for insertable
    residual class. Without the bonus, greedy converges to states with
    many solved pieces but mixed (non-insertable) residuals."""
    base = _count_solved_pieces(state)
    residual = analyze_residual(state)
    bonus = 0.0
    if residual.cycle_type == "solved":
        bonus = 100.0  # massively prefer solved
    elif residual.cycle_type in _WORTH_PURSUING_CLASSES:
        bonus = 5.0  # mild preference for insertable
    return base + bonus


def find_skeleton_greedy(
    scramble: list[str], history: list[str],
    *, axis: str = "UD", max_depth: int = 8, beam_width: int = 5,
) -> dict:
    """Greedy hill-climb to find an insertable skeleton.

    Move set is restricted to the DR group if the current state has DR
    solved on `axis`, else the EO-preserving group. The beam tracks the
    top `beam_width` states by solved-piece count at each depth. Any
    state whose residual is in the Tronto worth-pursuing set is recorded
    as a skeleton candidate.

    Returns:
      - skeletons: list of {moves, length, residual_class, num_unsolved,
        solved_pieces}, sorted by (length, -solved_pieces).
      - num_discarded: how many states had a non-insertable residual.
      - note: explanation of what was found.
    """
    if axis not in {"UD", "FB", "RL"}:
        return {"error": f"axis must be UD/FB/RL, got {axis!r}"}
    ax = Axis(axis)

    state = SOLVED.apply_alg(parse_alg(" ".join(scramble))) if scramble else SOLVED
    if history:
        state = state.apply_alg(parse_alg(" ".join(history)))

    if is_dr(state, ax):
        moves = _dr_group_moves(ax)
    elif is_eo_solved(state, ax):
        # Post-EO but pre-DR: use EO-preserving moves.
        flipping = {
            Axis.UD: (Face.F, Face.B),
            Axis.FB: (Face.L, Face.R),
            Axis.RL: (Face.U, Face.D),
        }[ax]
        moves = tuple(
            Move(f, t) for f in Face for t in Turn
            if not (f in flipping and t != Turn.HALF)
        )
    else:
        return {
            "error": (
                f"State must have EO solved on axis {axis} before greedy "
                f"skeleton search. Run eo_pattern_lookup first."
            ),
        }

    # Beam search with last-face filter, dedup via visited set. Score now
    # uses _greedy_score so insertable residuals are preferred.
    Frontier = list[tuple[State, list[Move], float, Face | None]]
    frontier: Frontier = [(state, [], _greedy_score(state), None)]
    seen: set[State] = {state}

    skeletons: list[dict] = []
    n_discarded = 0

    # If the starting state already has a worth-pursuing residual, record it.
    start_residual = analyze_residual(state)
    if start_residual.cycle_type in _WORTH_PURSUING_CLASSES:
        skeletons.append({
            "moves": [],
            "length": 0,
            "residual_class": start_residual.cycle_type,
            "num_unsolved": _count_unsolved(state),
            "solved_pieces": _count_solved_pieces(state),
        })

    for _ in range(max_depth):
        new_frontier: Frontier = []
        catcher_states: list[tuple[State, list[Move], float, Face | None]] = []
        for s, path, _, last_face in frontier:
            for m in moves:
                if last_face is not None and m.face == last_face:
                    continue
                child = s.apply(m)
                if child in seen:
                    continue
                seen.add(child)
                score = _greedy_score(child)
                new_frontier.append((child, path + [m], score, m.face))
                # Skeleton catcher: always retain insertable-residual states
                # in the next frontier, regardless of beam-trim, so we don't
                # lose them to higher-piece-count-but-mixed states.
                residual = analyze_residual(child)
                if residual.cycle_type in _WORTH_PURSUING_CLASSES:
                    catcher_states.append((child, path + [m], score, m.face))

        if not new_frontier:
            break
        new_frontier.sort(key=lambda x: -x[2])
        # Keep top-K plus the catcher states (insertable residuals always retained).
        frontier = new_frontier[:beam_width]
        # Add catcher states not already in beam.
        existing_states = {id(s) for s, _, _, _ in frontier}
        for cs in catcher_states:
            if id(cs[0]) not in existing_states:
                frontier.append(cs)

        for s, path, score, _ in frontier:
            residual = analyze_residual(s)
            if residual.cycle_type in _WORTH_PURSUING_CLASSES:
                skeletons.append({
                    "moves": [str(m) for m in path],
                    "length": len(path),
                    "residual_class": residual.cycle_type,
                    "num_unsolved": _count_unsolved(s),
                    "solved_pieces": _count_solved_pieces(s),
                })
            else:
                n_discarded += 1

    # De-dup by (residual_class, length, moves tuple)
    seen_skel: set[tuple] = set()
    unique: list[dict] = []
    for sk in skeletons:
        key = (sk["residual_class"], sk["length"], tuple(sk["moves"]))
        if key in seen_skel:
            continue
        seen_skel.add(key)
        unique.append(sk)
    unique.sort(key=lambda x: (x["length"], -x["solved_pieces"]))

    return {
        "skeletons": unique[:5],
        "num_discarded": n_discarded,
        "max_depth": max_depth,
        "beam_width": beam_width,
        "note": (
            f"Greedy search to depth {max_depth} (beam {beam_width}) found "
            f"{len(unique)} insertable skeletons, discarded {n_discarded} "
            f"states with non-insertable residuals. Pick one with low length "
            f"and matching residual_class to your insertion tool: "
            f"corner_3cycle -> derive_corner_3cycle; edge_3cycle/2e2e -> "
            f"manual derivation; else fall back to standard HTR finish."
        ),
    }


def _count_unsolved(state: State) -> int:
    n = 0
    for i in range(8):
        if state.cp[i] != i or state.co[i] != 0:
            n += 1
    for i in range(12):
        if state.ep[i] != i or state.eo[i] != 0:
            n += 1
    return n
