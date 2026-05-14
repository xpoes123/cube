"""Insertion finder for FMC skeletons.

An "insertion" is the technique of taking a near-solved skeleton (typically
22-26 moves) that leaves a small residual cycle of pieces, and inserting an
8-move commutator inside the skeleton so that the commutator's cycle
cancels the residual AND its moves merge well with the surrounding skeleton.

This module provides scaffolding:
  1. `analyze_residual(state)` — classify the leftover permutation
     (3-cycles, orientation cycles, parity, etc).
  2. `COMMUTATORS` — a small hardcoded library of canonical commutators
     with their cycle signatures.
  3. `find_insertions(skeleton, scramble)` — brute-force search across
     positions and commutators, return ranked options by post-cancellation
     length.

Naming/conventions:
- Corners are indexed 0..7 (URF, UFL, ULB, UBR, DFR, DLF, DBL, DRB).
- Edges are indexed 0..11 (see state.py).
- A "permutation cycle" `(a, b, c)` means the piece-content at slot a
  moves to slot b, b -> c, c -> a (i.e. the cycle in `state.cp` / `state.ep`).
- An "orientation cycle" lists the slot indices whose piece is correctly
  permuted but mis-twisted; the twist values come from `state.co` / EO.

This is intentionally a scaffold — it covers the common cases (pure
3-cycles of corners or edges) cleanly, and brute-forces position search.
Optimal insertion finding (multiple-insertion search, AUF-conjugation,
mirror/inverse variants of each commutator) is left to future work.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from cube.engine.cancellation import cancel_moves
from cube.engine.moves import Move
from cube.engine.notation import parse_alg
from cube.engine.state import SOLVED, State


# ---------- residual analysis ----------


CycleType = Literal[
    "solved",
    "corner_3cycle",
    "edge_3cycle",
    "corner_twist_2",      # two corners mis-twisted (CO sum 0 mod 3)
    "edge_flip_2",         # two edges flipped
    "corner_perm_other",   # other corner-perm case (2-2 swap, 5-cycle, etc.)
    "edge_perm_other",
    "mixed",               # mix of corner-perm and edge-perm cycles
    "complex",             # unclassified, multiple cycle types
]


@dataclass(frozen=True, slots=True)
class Residual:
    """Classification of an unsolved cube state's leftover pieces."""

    # Permutation cycles (non-fixed-point), corners then edges. Each cycle
    # lists slot indices in apply-order: slot a's piece -> slot b, b -> c,
    # ..., last -> a.
    corner_perm_cycles: tuple[tuple[int, ...], ...]
    edge_perm_cycles: tuple[tuple[int, ...], ...]
    # Slots whose piece is correctly permuted but mis-oriented. For corners,
    # `(slot, twist)` with twist in {1, 2}. For edges, `(slot, flip)` with
    # flip == 1.
    corner_twists: tuple[tuple[int, int], ...]
    edge_flips: tuple[tuple[int, int], ...]
    cycle_type: CycleType

    @property
    def is_solved(self) -> bool:
        return self.cycle_type == "solved"


def _perm_cycles(perm: tuple[int, ...]) -> tuple[tuple[int, ...], ...]:
    """Return the non-trivial cycles of `perm` as a tuple of slot-tuples.

    Convention: `perm[slot] = piece`. A cycle (a, b, c) means piece(a) -> b
    -> c -> a. We canonicalize by starting each cycle at its smallest slot.
    """
    n = len(perm)
    seen = [False] * n
    cycles: list[tuple[int, ...]] = []
    for start in range(n):
        if seen[start] or perm[start] == start:
            seen[start] = True
            continue
        # Walk the cycle. perm[slot] = piece means "this piece originated
        # at slot=piece"; we want forward cycle, i.e. piece(start) goes to
        # slot where perm[slot] == start... actually the more useful
        # interpretation: viewing perm as a function σ where σ(start) =
        # perm[start], the cycle is start -> σ(start) -> σ²(start) ... .
        # That's the cycle of "where does the content at slot s come from."
        # For FMC purposes either reading is fine — we just need a stable
        # canonical representation.
        cycle: list[int] = []
        slot = start
        while not seen[slot]:
            seen[slot] = True
            cycle.append(slot)
            slot = perm[slot]
        if len(cycle) > 1:
            # Rotate so smallest slot is first (canonical form).
            min_idx = cycle.index(min(cycle))
            cycle = cycle[min_idx:] + cycle[:min_idx]
            cycles.append(tuple(cycle))
    return tuple(cycles)


def analyze_residual(state: State) -> Residual:
    """Classify the leftover permutation/orientation of a (likely) near-
    solved state. Uses CP, CO, EP, and UD-axis EO only — multi-axis EO
    bookkeeping is irrelevant once a skeleton has reached HTR or beyond.
    """
    if state == SOLVED:
        return Residual((), (), (), (), "solved")

    cp_cycles = _perm_cycles(state.cp)
    ep_cycles = _perm_cycles(state.ep)

    # Orientation deltas only count for pieces that are correctly permuted
    # (so the residual is "pure twist" / "pure flip" on those slots).
    corner_twists = tuple(
        (i, state.co[i]) for i in range(8) if state.cp[i] == i and state.co[i] != 0
    )
    edge_flips = tuple(
        (i, state.eo[i]) for i in range(12) if state.ep[i] == i and state.eo[i] != 0
    )

    cycle_type: CycleType = _classify(cp_cycles, ep_cycles, corner_twists, edge_flips)
    return Residual(cp_cycles, ep_cycles, corner_twists, edge_flips, cycle_type)


def _classify(
    cp_cycles: tuple[tuple[int, ...], ...],
    ep_cycles: tuple[tuple[int, ...], ...],
    corner_twists: tuple[tuple[int, int], ...],
    edge_flips: tuple[tuple[int, int], ...],
) -> CycleType:
    has_corner_perm = bool(cp_cycles)
    has_edge_perm = bool(ep_cycles)
    has_corner_twist = bool(corner_twists)
    has_edge_flip = bool(edge_flips)

    nonempty = sum([has_corner_perm, has_edge_perm, has_corner_twist, has_edge_flip])
    if nonempty == 0:
        return "solved"
    if nonempty > 1:
        if (has_corner_perm or has_corner_twist) and (has_edge_perm or has_edge_flip):
            return "mixed"
        return "complex"
    if has_corner_perm:
        if len(cp_cycles) == 1 and len(cp_cycles[0]) == 3:
            return "corner_3cycle"
        return "corner_perm_other"
    if has_edge_perm:
        if len(ep_cycles) == 1 and len(ep_cycles[0]) == 3:
            return "edge_3cycle"
        return "edge_perm_other"
    if has_corner_twist:
        if len(corner_twists) == 2:
            return "corner_twist_2"
        return "complex"
    if has_edge_flip:
        if len(edge_flips) == 2:
            return "edge_flip_2"
        return "complex"
    return "complex"


# ---------- commutator library ----------


@dataclass(frozen=True, slots=True)
class Commutator:
    """A canonical commutator that performs a known cycle from SOLVED.

    `cycle_type` matches the `Residual.cycle_type` it targets. `signature`
    is the canonical cycle this commutator produces when applied to SOLVED
    (e.g. for a 3-cycle of corners, the corner slots in apply-order).
    """

    name: str
    moves_str: str           # WCA notation, e.g. "R U R' U' R' F R F'"
    cycle_type: CycleType
    signature: tuple[tuple[int, ...], ...]  # slot cycles (in canonical form)
    # Affected slots (handy for matching). For corner_twist_2 / edge_flip_2,
    # signature is empty and `affected_slots` lists the twisted/flipped slots.
    affected_slots: tuple[int, ...] = ()

    @property
    def moves(self) -> tuple[Move, ...]:
        return tuple(parse_alg(self.moves_str))

    def __len__(self) -> int:
        return len(self.moves)


def _signature_for(moves_str: str) -> Residual:
    """Apply moves to SOLVED and return its residual classification.

    Useful for both library construction and tests — the library's
    `signature` field is verified against this at load.
    """
    state = SOLVED.apply_alg(parse_alg(moves_str))
    return analyze_residual(state)


# --- Library entries.
#
# Each entry is a well-known 8-move commutator (or close). We name them by
# their cycle, and the `signature` is filled in by applying to SOLVED.
# Mirror/inverse/AUF variants are not enumerated — adding them is a clean
# next step. The library is intentionally small for the v0 scaffold.
#
# A note on corner indexing for the curious:
#   0=URF, 1=UFL, 2=ULB, 3=UBR, 4=DFR, 5=DLF, 6=DBL, 7=DRB
#
# Edge indexing:
#   0=UR, 1=UF, 2=UL, 3=UB, 4=DR, 5=DF, 6=DL, 7=DB, 8=FR, 9=FL, 10=BL, 11=BR


_RAW_COMMUTATORS: tuple[tuple[str, str, CycleType], ...] = (
    # --- Pure corner 3-cycles (8 face-turn moves, classic FMC insertions).
    # These are [A, B] = A B A' B' commutators where A is a setup move and
    # B is a "interchange" — the canonical commutator structure.

    # [R U' R', D]: cycles URF/DFR/DLF. Standard FMC right-side comm.
    ("corner_3c_RUR_D_a", "R U' R' D R U R' D'", "corner_3cycle"),

    # [R U R', D]: cycles UFL/DFR/DLF. Same machinery, different setup.
    ("corner_3c_RUR_D_b", "R U R' D R U' R' D'", "corner_3cycle"),

    # Niklas variants — 8-move pure 3-corner cycles on the U layer.
    # Canonical small-piece-cycle insertion.
    ("niklas", "R U' L' U R' U' L U", "corner_3cycle"),
    ("niklas_mirror", "L' U R U' L U R' U'", "corner_3cycle"),
    ("niklas_inv", "U' L' U R U' L U R'", "corner_3cycle"),

    # Mid-bottom 3-cycle: [R' D R, U]. Cycles URF/DRB/DFR or similar.
    ("corner_3c_RDR_U", "R' D R U R' D' R U'", "corner_3cycle"),

    # --- Pure edge 3-cycles. Face-turn-only edge 3-cycles are inherently
    # longer (10+ moves) than corner ones — the U-perms are the cleanest.

    # U-perm A — 11-move edge 3-cycle of UF/UR/UL (or rotation thereof).
    ("u_perm_a", "R2 U R U R' U' R' U' R' U R'", "edge_3cycle"),

    # U-perm B — inverse cycle direction.
    ("u_perm_b", "R U' R U R U R U' R' U' R2", "edge_3cycle"),

    # --- Mixed cycles (a permutation + an orientation, or 2-2 swaps).
    # Sune / anti-sune permute three corners AND flip the fourth in their
    # canonical form. Useful when the residual is itself mixed.
    ("sune", "R U R' U R U2 R'", "complex"),
    ("anti_sune", "R U2 R' U' R U' R'", "complex"),
)


def _make_commutator(name: str, moves_str: str, declared_type: CycleType) -> Commutator:
    residual = _signature_for(moves_str)
    sig = residual.corner_perm_cycles + residual.edge_perm_cycles
    affected = tuple(
        sorted(set(
            [i for cycle in sig for i in cycle]
            + [s for s, _ in residual.corner_twists]
            + [s for s, _ in residual.edge_flips]
        ))
    )
    ct = residual.cycle_type if declared_type == "complex" else declared_type
    return Commutator(
        name=name, moves_str=moves_str, cycle_type=ct,
        signature=sig, affected_slots=affected,
    )


def _build_library() -> tuple[Commutator, ...]:
    """Build the live library. Also auto-derives inverse commutators (which
    perform the same cycle in the opposite direction) for pure 3-cycle
    entries — these are needed almost as often as the originals and free."""
    out: list[Commutator] = []
    seen_moves: set[str] = set()
    for name, moves_str, declared_type in _RAW_COMMUTATORS:
        comm = _make_commutator(name, moves_str, declared_type)
        if comm.moves_str in seen_moves:
            continue
        seen_moves.add(comm.moves_str)
        out.append(comm)
        # Auto-derive inverses for pure 3-cycle entries — they cycle the
        # same three pieces in the opposite direction, an obvious and
        # important variant.
        if comm.cycle_type in ("corner_3cycle", "edge_3cycle"):
            inv_moves = [m.inverse() for m in reversed(comm.moves)]
            inv_str = " ".join(str(m) for m in inv_moves)
            if inv_str in seen_moves:
                continue
            seen_moves.add(inv_str)
            out.append(_make_commutator(
                f"{comm.name}_inv", inv_str, comm.cycle_type,
            ))
    return tuple(out)


COMMUTATORS: tuple[Commutator, ...] = _build_library()


def commutators_for(cycle_type: CycleType) -> tuple[Commutator, ...]:
    """Return library entries whose own residual matches `cycle_type`.

    For "complex" or "mixed" residuals, returns the full library (the
    caller will brute-force try everything anyway).
    """
    if cycle_type in ("complex", "mixed"):
        return COMMUTATORS
    return tuple(c for c in COMMUTATORS if c.cycle_type == cycle_type)


# ---------- insertion finder ----------


@dataclass(frozen=True, slots=True)
class InsertionOption:
    """One candidate insertion result. Ranked by `final_length`."""

    commutator: Commutator
    position: int                          # insertion index in the skeleton
    raw_length: int                        # len(skeleton) + len(commutator)
    final_length: int                      # post-cancellation length
    final_moves: tuple[Move, ...]          # cancelled skeleton+insertion
    solved: bool                           # does the final cube reach SOLVED?

    @property
    def savings(self) -> int:
        return self.raw_length - self.final_length


def find_insertions(
    skeleton: list[Move] | tuple[Move, ...],
    scramble: list[Move] | tuple[Move, ...],
    library: tuple[Commutator, ...] | None = None,
    only_solving: bool = True,
    top_k: int | None = None,
) -> list[InsertionOption]:
    """Brute-force insertion search.

    For every (position, commutator) pair, splice the commutator in and
    measure the post-cancellation length. We verify each candidate by
    applying scramble + (skeleton with insertion) to SOLVED and checking
    SOLVED.

    Args:
      skeleton: the move sequence that the user has produced.
      scramble: the original scramble (used to verify SOLVED).
      library: which commutators to try. Defaults to `COMMUTATORS`.
      only_solving: drop options that don't actually reach SOLVED.
      top_k: cap the returned list.

    Returns options sorted ascending by `final_length` (then by `savings`).
    """
    if library is None:
        library = COMMUTATORS

    skel = list(skeleton)
    scr = list(scramble)
    options: list[InsertionOption] = []

    for comm in library:
        comm_moves = list(comm.moves)
        for pos in range(len(skel) + 1):
            spliced = skel[:pos] + comm_moves + skel[pos:]
            cancelled = cancel_moves(spliced)
            final_state = SOLVED.apply_alg(scr + cancelled)
            is_solved = final_state == SOLVED
            if only_solving and not is_solved:
                continue
            options.append(InsertionOption(
                commutator=comm,
                position=pos,
                raw_length=len(skel) + len(comm_moves),
                final_length=len(cancelled),
                final_moves=tuple(cancelled),
                solved=is_solved,
            ))

    options.sort(key=lambda o: (o.final_length, -o.savings, o.position))
    if top_k is not None:
        options = options[:top_k]
    return options


def find_insertions_for_skeleton(
    skeleton_moves: list[Move] | tuple[Move, ...],
    scramble: list[Move] | tuple[Move, ...],
    top_k: int = 10,
) -> tuple[Residual, list[InsertionOption]]:
    """Convenience wrapper: also returns the classified residual.

    If the skeleton already solves the scramble, returns an empty option
    list with a "solved" residual.
    """
    residual_state = SOLVED.apply_alg(list(scramble) + list(skeleton_moves))
    residual = analyze_residual(residual_state)
    if residual.is_solved:
        return residual, []

    # Narrow the library by residual type when possible — but always fall
    # back to the full library if the narrow set finds nothing, since the
    # geometry of conjugation across insertion positions can let a
    # commutator solve a residual that doesn't textually match its
    # canonical signature.
    lib = commutators_for(residual.cycle_type)
    options = find_insertions(skeleton_moves, scramble, library=lib, top_k=top_k)
    if not options:
        options = find_insertions(skeleton_moves, scramble, top_k=top_k)
    return residual, options
