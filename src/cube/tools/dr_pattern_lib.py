"""Memorized DR pattern library.

Same shape as the EO pattern library, one level deeper. For every reachable
(corner-orientation, slice-membership) pattern within the EO-preserving
subgroup on each axis, the library stores an optimal-length move sequence
to reach DR. O(1) lookup at runtime — recognition, not search.

Key per axis: (axis_name, co_tuple, slice_marker_tuple) where
- co_tuple is the 8-corner twist array under that axis's convention (0/1/2)
- slice_marker_tuple is 12 bits: bit i = 1 iff slot i currently contains
  one of the axis-perpendicular slice edges (E-slice for UD, etc.)

Faithful-quotient property: under any EO-preserving move on the axis,
new (co_tuple, marker_tuple) depends only on the current pair plus the
move, NOT on the underlying full state. So a single BFS in this reduced
space enumerates every reachable DR pre-image, optimally.

State space per axis: 3^7 (co, parity-constrained) × C(12,4) = 2187 × 495 ≈ 1.08M.
"""

from __future__ import annotations

import pickle
from collections import deque
from pathlib import Path

from cube.classifier.features import Axis
from cube.engine.facelet import CORNER_COLORS, CORNER_FACELETS, face_of
from cube.engine.moves import ALL_MOVES, Face, Move, Turn
from cube.engine.notation import parse_alg
from cube.engine.state import SOLVED, State, _FACE_TURN_CW

_AXIS_LOOKUP = {a.value: a for a in Axis}
# v33: legacy pickle path kept for save_library() — agent only ever READS
# from the JSON memory now. The 3.2M-entry pickle was deleted in v32.
LIBRARY_PATH = Path("checkpoints/dr_pattern_library.pkl")
MEMORY_JSON_PATH = Path("data/memory/dr_patterns.json")

# (axis_name, co_tuple, marker_tuple) -> list[str] moves to reach DR
DRLibrary = dict[tuple[str, tuple[int, ...], tuple[int, ...]], list[str]]

_LIBRARY: DRLibrary | None = None


# ---------------------------------------------------------------------------
# Axis-orientation tables (cubie/position slot of each axis color)
# ---------------------------------------------------------------------------
# face indices: U=0 R=1 F=2 D=3 L=4 B=5 (facelet.py)
_UD_FACES = frozenset({0, 3})
_FB_FACES = frozenset({2, 5})
_RL_FACES = frozenset({1, 4})


def _axis_slot_in_cubie(cubie: int, axis_faces: frozenset[int]) -> int:
    colors = CORNER_COLORS[cubie]
    return next(s for s in range(3) if colors[s] in axis_faces)


def _axis_face_pos_slot(pos: int, axis_faces: frozenset[int]) -> int:
    facelets = CORNER_FACELETS[pos]
    return next(s for s in range(3) if face_of(facelets[s]) in axis_faces)


_FB_SLOT_IN_CUBIE = tuple(_axis_slot_in_cubie(c, _FB_FACES) for c in range(8))
_RL_SLOT_IN_CUBIE = tuple(_axis_slot_in_cubie(c, _RL_FACES) for c in range(8))
_UD_SLOT_IN_CUBIE = tuple(_axis_slot_in_cubie(c, _UD_FACES) for c in range(8))

_FB_FACE_POS_SLOT = tuple(_axis_face_pos_slot(p, _FB_FACES) for p in range(8))
_RL_FACE_POS_SLOT = tuple(_axis_face_pos_slot(p, _RL_FACES) for p in range(8))
_UD_FACE_POS_SLOT = tuple(_axis_face_pos_slot(p, _UD_FACES) for p in range(8))


# Slice edge sets (indices into ep / slot positions)
_E_SLICE = frozenset({8, 9, 10, 11})  # perp to UD
_S_SLICE = frozenset({0, 2, 4, 6})    # perp to FB
_M_SLICE = frozenset({1, 3, 5, 7})    # perp to RL

_SLICE_BY_AXIS = {
    Axis.UD: _E_SLICE,
    Axis.FB: _S_SLICE,
    Axis.RL: _M_SLICE,
}

# Solved marker: slice edges in their own slice positions
_SOLVED_MARKER = {
    Axis.UD: tuple(1 if i in _E_SLICE else 0 for i in range(12)),
    Axis.FB: tuple(1 if i in _S_SLICE else 0 for i in range(12)),
    Axis.RL: tuple(1 if i in _M_SLICE else 0 for i in range(12)),
}


# ---------------------------------------------------------------------------
# Reduced-state transitions
# ---------------------------------------------------------------------------
# For each axis, build a `dco_axis` table per face that gives the corner-twist
# delta on the axis-relative CO under that face's CW turn.
#
# Derivation: with co_ax[p] = (AXIS_FACE_POS_SLOT[p] - AXIS_SLOT_IN_CUBIE[cp[p]]
#                              - co_ud[p]) mod 3,
# applying a face's CW (cycle, dco_ud) gives
#   new_co_ax[dst] = co_ax[src] + (FACE_POS_SLOT[dst] - FACE_POS_SLOT[src]
#                                  - dco_ud[i]) mod 3
# which is the desired delta. It depends only on the face, not on cubies.


def _build_dco_axis(face_pos_slot: tuple[int, ...]) -> dict[Face, tuple[int, ...]]:
    table = {}
    for face in Face:
        cycle, dco_ud, _, _, _, _ = _FACE_TURN_CW[face]
        deltas = []
        for i in range(4):
            src = cycle[i]
            dst = cycle[(i + 1) % 4]
            d = (face_pos_slot[dst] - face_pos_slot[src] - dco_ud[i]) % 3
            deltas.append(d)
        table[face] = tuple(deltas)
    return table


_DCO_UD = _build_dco_axis(_UD_FACE_POS_SLOT)  # equals dco_ud from _FACE_TURN_CW
_DCO_FB = _build_dco_axis(_FB_FACE_POS_SLOT)
_DCO_RL = _build_dco_axis(_RL_FACE_POS_SLOT)

_DCO_BY_AXIS = {Axis.UD: _DCO_UD, Axis.FB: _DCO_FB, Axis.RL: _DCO_RL}


# EO-preserving move sets per axis (flipping quarters excluded)
_FLIPPING_FACES = {
    Axis.UD: frozenset({Face.F, Face.B}),
    Axis.FB: frozenset({Face.L, Face.R}),
    Axis.RL: frozenset({Face.U, Face.D}),
}

_EO_PRESERVING_BY_AXIS = {
    axis: tuple(
        Move(f, t) for f in Face for t in Turn
        if not (f in _FLIPPING_FACES[axis] and t != Turn.HALF)
    )
    for axis in Axis
}


def _apply_to_reduced(
    co: tuple[int, ...],
    marker: tuple[int, ...],
    move: Move,
    axis: Axis,
) -> tuple[tuple[int, ...], tuple[int, ...]]:
    cycle_c, _, cycle_e, _, _, _ = _FACE_TURN_CW[move.face]
    dco = _DCO_BY_AXIS[axis][move.face]
    new_co = list(co)
    new_marker = list(marker)
    for _ in range(move.turn):
        next_co = new_co.copy()
        next_marker = new_marker.copy()
        for i in range(4):
            src = cycle_c[i]
            dst = cycle_c[(i + 1) % 4]
            next_co[dst] = (new_co[src] + dco[i]) % 3
        for i in range(4):
            src = cycle_e[i]
            dst = cycle_e[(i + 1) % 4]
            next_marker[dst] = new_marker[src]
        new_co = next_co
        new_marker = next_marker
    return tuple(new_co), tuple(new_marker)


def _inverse_move(m: Move) -> Move:
    return Move(m.face, Turn(4 - m.turn))


# ---------------------------------------------------------------------------
# Reading the reduced state from a full State
# ---------------------------------------------------------------------------


def _axis_co_from_state(state: State, axis: Axis) -> tuple[int, ...]:
    """Compute the 8-corner axis-relative CO array.

    Convention: co_ax[p] = (axis_face_pos_slot[p] - axis_slot_in_cubie[cp[p]]
                            - co_ud[p]) mod 3.
    DR-aligned on axis iff co_ax[p] == 0 for all p. For UD this happens to
    equal (-state.co) mod 3 (face_pos_slot and slot_in_cubie are both 0 for
    UD); identical zero-set as state.co, but the BFS must use the same sign
    convention, so we always derive from the formula.
    """
    if axis == Axis.UD:
        face_slot = _UD_FACE_POS_SLOT
        in_cubie = _UD_SLOT_IN_CUBIE
    elif axis == Axis.FB:
        face_slot = _FB_FACE_POS_SLOT
        in_cubie = _FB_SLOT_IN_CUBIE
    else:
        face_slot = _RL_FACE_POS_SLOT
        in_cubie = _RL_SLOT_IN_CUBIE
    return tuple(
        (face_slot[p] - in_cubie[state.cp[p]] - state.co[p]) % 3
        for p in range(8)
    )


def _slice_marker_from_state(state: State, axis: Axis) -> tuple[int, ...]:
    slice_set = _SLICE_BY_AXIS[axis]
    return tuple(1 if state.ep[i] in slice_set else 0 for i in range(12))


# ---------------------------------------------------------------------------
# Library load / save
# ---------------------------------------------------------------------------


def _ensure_loaded() -> DRLibrary:
    """v33: load the small (~3,657-entry) DR memory from JSON.

    Format: `data/memory/dr_patterns.json` with keys
    "axis|co_csv|marker_csv" → list of move strings. Covers DR states
    within 4 moves of solved — the human-visualization scope. States
    deeper than that are NOT in the library; callers should fall back
    to brain_suggest (the trained policy) or commit setup moves and
    re-query from a closer state.
    """
    global _LIBRARY
    if _LIBRARY is not None:
        return _LIBRARY
    import json
    if not MEMORY_JSON_PATH.exists():
        _LIBRARY = {}
        return _LIBRARY
    try:
        raw = json.loads(MEMORY_JSON_PATH.read_text())
    except (json.JSONDecodeError, OSError):
        _LIBRARY = {}
        return _LIBRARY
    lib: DRLibrary = {}
    for str_key, moves in raw.items():
        try:
            axis, co_csv, marker_csv = str_key.split("|")
            co = tuple(int(x) for x in co_csv.split(","))
            marker = tuple(int(x) for x in marker_csv.split(","))
            lib[(axis, co, marker)] = list(moves)
        except (ValueError, KeyError):
            continue
    _LIBRARY = lib
    return _LIBRARY


def save_library(library: DRLibrary, path: Path = LIBRARY_PATH) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("wb") as f:
        pickle.dump(library, f)


# ---------------------------------------------------------------------------
# Lookup tool
# ---------------------------------------------------------------------------


def dr_pattern_lookup(
    scramble: list[str],
    history: list[str],
    *,
    axis: str,
) -> dict:
    """Recall a memorized DR completion for the current state on `axis`.

    Preconditions: EO on `axis` must already be solved (run eo_pattern_lookup
    + apply_moves first). If it isn't, returns an error.

    Returns:
      - if hit: {'found': 1, 'options': [{'moves': [...], 'length': N}],
                 'cached': True}
      - if miss: {'found': 0, ..., 'note': 'pattern not in library'}
    """
    if axis not in _AXIS_LOOKUP:
        return {"error": f"axis must be UD/FB/RL; got {axis!r}"}
    ax = _AXIS_LOOKUP[axis]

    state = SOLVED.apply_alg(parse_alg(" ".join(scramble))) if scramble else SOLVED
    if history:
        state = state.apply_alg(parse_alg(" ".join(history)))

    from cube.classifier.features import is_eo_solved, is_dr
    if not is_eo_solved(state, ax):
        return {
            "error": f"EO not yet solved on axis {axis}; run eo_pattern_lookup "
                     f"+ apply_moves first."
        }

    if is_dr(state, ax):
        return {
            "found": 1,
            "options": [{"moves": [], "length": 0}],
            "cached": True,
            "note": "Already in DR on this axis.",
        }

    co = _axis_co_from_state(state, ax)
    marker = _slice_marker_from_state(state, ax)
    key = (axis, co, marker)
    library = _ensure_loaded()
    if key in library:
        moves = library[key]
        return {
            "found": 1,
            "options": [{"moves": list(moves), "length": len(moves)}],
            "cached": True,
            "note": f"Recognized DR pattern — playing memorized {len(moves)}-move completion.",
        }
    return {
        "found": 0,
        "options": [],
        "cached": False,
        "note": (
            f"DR pattern not in library for axis {axis}. "
            f"Fall back to find_dr_via_trigger."
        ),
    }


# ---------------------------------------------------------------------------
# Builder: forward BFS in reduced state per axis
# ---------------------------------------------------------------------------


def build_dr_library(*, max_depth: int = 16, verbose: bool = True) -> DRLibrary:
    """Forward BFS from DR-solved in (co, marker) reduced space per axis.

    Each visited state's optimal solver = inverse of the forward path.
    """
    import time
    library: DRLibrary = {}
    t0 = time.time()

    for axis in [Axis.UD, Axis.FB, Axis.RL]:
        axis_name = axis.value
        moves = _EO_PRESERVING_BY_AXIS[axis]
        solved_co = (0,) * 8
        solved_marker = _SOLVED_MARKER[axis]
        start_key = (solved_co, solved_marker)

        # path_to_state: reduced_state -> tuple of Move objects (forward path)
        path_to_state: dict[tuple, tuple[Move, ...]] = {start_key: ()}
        # Library record for the solved state itself
        library[(axis_name, solved_co, solved_marker)] = []
        frontier: deque[tuple] = deque([start_key])
        explored = 0
        depth_hist = [0] * (max_depth + 1)
        depth_hist[0] = 1

        while frontier:
            cur = frontier.popleft()
            cur_path = path_to_state[cur]
            if len(cur_path) >= max_depth:
                continue
            last_face = cur_path[-1].face if cur_path else None
            cur_co, cur_marker = cur
            for m in moves:
                if last_face is not None and m.face == last_face:
                    continue
                child = _apply_to_reduced(cur_co, cur_marker, m, axis)
                if child in path_to_state:
                    continue
                new_path = cur_path + (m,)
                path_to_state[child] = new_path
                solver = tuple(reversed([_inverse_move(mm) for mm in new_path]))
                library[(axis_name, child[0], child[1])] = [str(mm) for mm in solver]
                depth_hist[len(new_path)] += 1
                explored += 1
                frontier.append(child)
        if verbose:
            print(
                f"  axis {axis_name}: {explored} reachable DR states, "
                f"library now {len(library)} entries, {time.time() - t0:.1f}s"
            )
            nonzero = [(d, n) for d, n in enumerate(depth_hist) if n > 0]
            print(f"    depth histogram: {nonzero}")
    return library


__all__ = [
    "dr_pattern_lookup",
    "build_dr_library",
    "save_library",
    "LIBRARY_PATH",
]
