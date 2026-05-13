"""Phase taxonomy for FMC reconstruction segmentation.

Canonical phases capture the structural milestones in a solve. The taxonomy is
DR-dominant because modern FMC is DR-dominant, but the BLOCK and EOLINE phases
keep blockbuilding and ZZ-style solves representable. Always carries the
author's raw label string alongside the canonical phase so we don't lose
information when an author writes "DR, 4a1" or "M + S slice".
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum

from cube.corpus.types import Reconstruction
from cube.engine.notation import NissAlg
from cube.engine.state import State


class Phase(str, Enum):
    EO = "eo"               # edge orientation reached
    DR = "dr"               # domino reduction reached (incl. DR trigger move)
    HTR = "htr"             # half-turn reduction reached
    SLICE = "slice"         # M/S/E slice toward solved (typically post-HTR)
    FINISH = "finish"       # final completion to solved
    BLOCK = "block"         # blockbuilding phase (2x2x2, 2x2x3, F2L-1)
    EOLINE = "eoline"       # ZZ-style EOLine
    INSERTION = "insertion" # commutator/conjugate inserted into skeleton
    SKELETON = "skeleton"   # explicit skeleton declaration (pre-insertion)
    PRE_EO = "pre_eo"       # moves before any milestone (often inverse-side scouting)
    UNKNOWN = "unknown"     # author label couldn't be canonicalized


class Method(str, Enum):
    DR = "dr"                       # EO -> DR -> HTR -> finish
    BLOCKBUILDING = "blockbuilding" # 2x2x2 -> 2x2x3 -> F2L-1 -> LL
    ZZ = "zz"                       # EOLine -> F2L -> LL
    CORNERS_FIRST = "corners_first" # corners -> edges
    UNKNOWN = "unknown"


@dataclass(frozen=True, slots=True)
class PhaseSegment:
    """One phase of a reconstruction's skeleton.

    `moves` is NISS-preserving (the author may have used parens to apply moves
    on the inverse scramble within this phase). `state_at_end` is the cube
    state after applying all phases up to and including this one (in flat
    form) to the post-scramble state.
    """

    phase: Phase
    raw_label: str           # exact author string, e.g. "DR, 4a1"
    moves: NissAlg           # the moves in this phase, NISS preserved
    state_at_end: State      # cube state after this phase (cumulative)
    phase_move_count: int    # moves added by this phase
    cumulative_count: int    # total moves through end of this phase
    # If the author annotated a count, we keep it for cross-checking.
    author_cumulative: int | None = None
    author_phase_count: int | None = None


@dataclass(frozen=True, slots=True)
class SegmentedReconstruction:
    """A Reconstruction enriched with phase segmentation and inferred method."""

    reconstruction: Reconstruction
    segments: tuple[PhaseSegment, ...]
    method: Method
    # Source of the segmentation: "comment" if author-labeled, "state" if
    # derived from milestone detection on the cube state.
    source: str
    # Cross-validation report: list of (phase_index, issue_description) for
    # disagreements between author labels and state-based detection.
    issues: tuple[str, ...] = field(default_factory=tuple)
