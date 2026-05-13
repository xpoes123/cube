"""Sticker (facelet) representation of cube state.

54 stickers, 6 faces × 9 positions. Face order: U R F D L B (Kociemba's
standard). Each face indexed 0-8 in reading order (top-left to bottom-right
as viewed from outside that face).

Used for multi-axis EO/DR detection (where the cubie representation's
convention isn't directly applicable) and for the eventual web visualizer.

The cubie-to-facelet mapping is derived once and verified against pycuber
for every face turn.
"""

from __future__ import annotations

from cube.engine.state import State

# Face indices in the 54-element facelet array
U, R, F, D, L, B = 0, 1, 2, 3, 4, 5
FACE_NAMES = "URFDLB"


def face_of(facelet_idx: int) -> int:
    """Which face does this facelet index belong to (0-5 = U/R/F/D/L/B)."""
    return facelet_idx // 9


# Per-corner-position, the 3 facelet indices in (slot 0, slot 1, slot 2) order.
# Slot 0 = U-or-D facelet, slot 1 = CW-next from slot 0, slot 2 = CW-after.
# CW order at each corner (viewed from outside):
#   URF: U->R->F     UFL: U->F->L     ULB: U->L->B     UBR: U->B->R
#   DFR: D->F->R     DLF: D->L->F     DBL: D->B->L     DRB: D->R->B
CORNER_FACELETS: tuple[tuple[int, int, int], ...] = (
    (8, 9, 20),    # URF: U9 R1 F3
    (6, 18, 38),   # UFL: U7 F1 L3
    (0, 36, 47),   # ULB: U1 L1 B3
    (2, 45, 11),   # UBR: U3 B1 R3
    (29, 26, 15),  # DFR: D3 F9 R7
    (27, 44, 24),  # DLF: D1 L9 F7
    (33, 53, 42),  # DBL: D7 B9 L7
    (35, 17, 51),  # DRB: D9 R9 B7
)

# Per-edge-position, the 2 facelet indices in (slot 0, slot 1) order.
# Slot 0 = U-or-D for U/D layer edges, F-or-B for E-slice edges. Slot 1 = the
# other slot of the position.
EDGE_FACELETS: tuple[tuple[int, int], ...] = (
    (5, 10),   # UR: U6 R2
    (7, 19),   # UF: U8 F2
    (3, 37),   # UL: U4 L2
    (1, 46),   # UB: U2 B2
    (32, 16),  # DR: D6 R8
    (28, 25),  # DF: D2 F8
    (30, 43),  # DL: D4 L8
    (34, 52),  # DB: D8 B8
    (23, 12),  # FR: F6 R4
    (21, 41),  # FL: F4 L6
    (50, 39),  # BL: B6 L4
    (48, 14),  # BR: B4 R6
)

# Color of each slot for each cubie type, in slot 0/1/2 order matching
# CORNER_FACELETS/EDGE_FACELETS slot order.
CORNER_COLORS: tuple[tuple[int, int, int], ...] = (
    (U, R, F),  # URF cubie
    (U, F, L),  # UFL
    (U, L, B),  # ULB
    (U, B, R),  # UBR
    (D, F, R),  # DFR
    (D, L, F),  # DLF
    (D, B, L),  # DBL
    (D, R, B),  # DRB
)

EDGE_COLORS: tuple[tuple[int, int], ...] = (
    (U, R),  # UR
    (U, F),  # UF
    (U, L),  # UL
    (U, B),  # UB
    (D, R),  # DR
    (D, F),  # DF
    (D, L),  # DL
    (D, B),  # DB
    (F, R),  # FR
    (F, L),  # FL
    (B, L),  # BL
    (B, R),  # BR
)


CORNER_COLORSET_TO_TYPE: dict[frozenset[int], int] = {
    frozenset(colors): idx for idx, colors in enumerate(CORNER_COLORS)
}
EDGE_COLORSET_TO_TYPE: dict[frozenset[int], int] = {
    frozenset(colors): idx for idx, colors in enumerate(EDGE_COLORS)
}


def to_facelets(state: State) -> tuple[int, ...]:
    """Convert cubie state to 54-element facelet array (face labels 0-5)."""
    facelets = [0] * 54
    # Centers (face label at index 4 of each face = center)
    for face in range(6):
        facelets[face * 9 + 4] = face
    # Corners
    for pos in range(8):
        cubie = state.cp[pos]
        orient = state.co[pos]
        cubie_colors = CORNER_COLORS[cubie]
        facelet_slots = CORNER_FACELETS[pos]
        for slot in range(3):
            color = cubie_colors[(slot - orient) % 3]
            facelets[facelet_slots[slot]] = color
    # Edges
    for pos in range(12):
        cubie = state.ep[pos]
        orient = state.eo[pos]
        cubie_colors = EDGE_COLORS[cubie]
        facelet_slots = EDGE_FACELETS[pos]
        for slot in range(2):
            color = cubie_colors[(slot + orient) % 2]
            facelets[facelet_slots[slot]] = color
    return tuple(facelets)


def from_facelets(facelets: tuple[int, ...]) -> State:
    """Recover full cubie state from a 54-element facelet array.

    Inverse of `to_facelets`. Used for state I/O and for axis-EO/DR detection
    (we rotate the facelets and re-recover state in the new frame).

    The recovery exploits the fact that every edge and corner cubie has a
    unique multiset of colors. So we identify the cubie at each position by
    its color set, then determine orientation by which slot holds the cubie's
    "slot 0" color (the U/D color for U/D-layer cubies, the F/B color for
    E-slice cubies).
    """
    cp = [0] * 8
    co = [0] * 8
    ep = [0] * 12
    eo = [0] * 12

    for pos in range(8):
        slot_facelets = CORNER_FACELETS[pos]
        colors_at_slots = tuple(facelets[s] for s in slot_facelets)
        cubie = CORNER_COLORSET_TO_TYPE[frozenset(colors_at_slots)]
        cp[pos] = cubie
        slot0_color = CORNER_COLORS[cubie][0]
        # The slot where the cubie's slot-0 color landed = the cubie's orientation.
        for slot_idx in range(3):
            if colors_at_slots[slot_idx] == slot0_color:
                co[pos] = slot_idx
                break

    for pos in range(12):
        slot_facelets = EDGE_FACELETS[pos]
        colors_at_slots = tuple(facelets[s] for s in slot_facelets)
        cubie = EDGE_COLORSET_TO_TYPE[frozenset(colors_at_slots)]
        ep[pos] = cubie
        slot0_color = EDGE_COLORS[cubie][0]
        # eo=0 iff cubie's slot 0 color is at position's slot 0; else eo=1.
        eo[pos] = 0 if colors_at_slots[0] == slot0_color else 1

    return State(cp=tuple(cp), co=tuple(co), ep=tuple(ep), eo=tuple(eo))
