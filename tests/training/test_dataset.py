"""Training data pipeline tests."""

import json

from cube.corpus.record import segmented_to_dict
from cube.corpus.sources.api333fm import submission_to_reconstruction
from cube.engine.notation import format_alg
from cube.segmenter import segment
from cube.training import (
    examples_from_segmented,
    iter_examples_from_jsonl,
    record_to_examples,
)


_REAL_SUBMISSION = {
    "id": 45821,
    "solution": "U F L R' U B' F' L2 U2 F R2 D2 B2 U2 L' D2 B2 L R D2 B'",
    "inverse": False,
    "comment": (
        "U F L R' U//EO (5/5)\n"
        "(B) F2 D2 L2 B//DR, 4a1 (5/10)\n"
        "(D2 R2 U2 B2 R)//HTR (5/15)\n"
        "(U2 F2 U2 L2)//M + S slice (4/19)\n"
    ),
    "competitionId": 3006,
    "userId": 635,
    "scramble": {
        "scramble": "R' U' F D R F2 D L F D2 F2 L' U R' L2 D' R2 F2 R2 D L2 U2 R' U' F",
    },
}
_REAL_RECON = {"user": {"id": 635, "name": "Wong"}}


def make_segmented():
    rec = submission_to_reconstruction(
        _REAL_SUBMISSION, recon=_REAL_RECON, competition_name="FMC 2024"
    )
    return segment(rec)


def test_one_example_per_flat_move():
    """Number of examples = length of flat solution."""
    seg = make_segmented()
    examples = examples_from_segmented(seg)
    assert len(examples) == seg.reconstruction.length


def test_first_example_starts_at_scrambled_state():
    """The first example's state_before equals (scramble applied to SOLVED)."""
    from cube.engine.state import SOLVED

    seg = make_segmented()
    examples = examples_from_segmented(seg)
    expected = SOLVED.apply_alg(seg.reconstruction.scramble)
    assert examples[0].state_before == expected


def test_state_evolution_matches_target_moves():
    """Applying each example's target_move to its state_before yields the next
    example's state_before (consistency check)."""
    seg = make_segmented()
    examples = examples_from_segmented(seg)
    for i in range(len(examples) - 1):
        next_state = examples[i].state_before.apply(examples[i].target_move)
        assert next_state == examples[i + 1].state_before


def test_history_length_matches_move_index():
    seg = make_segmented()
    examples = examples_from_segmented(seg)
    for i, ex in enumerate(examples):
        assert len(ex.history) == i
        assert ex.move_index == i


def test_phase_labels_cover_skeleton_moves():
    """Wong's skeleton is 19 moves; flat solution is 21 (with insertions).
    The first 19 moves should have phase labels; last 2 should be None."""
    seg = make_segmented()
    examples = examples_from_segmented(seg)
    # Wong's cumulative phase counts: 5, 10, 15, 19. So moves 0-18 have phases.
    for i in range(19):
        assert examples[i].phase is not None, f"move {i} should have a phase"
    # Moves 19, 20 (the 2 extra from insertions) have no phase.
    assert examples[19].phase is None
    assert examples[20].phase is None


def test_phase_eo_for_first_5_moves():
    seg = make_segmented()
    examples = examples_from_segmented(seg)
    from cube.segmenter import Phase
    for i in range(5):
        assert examples[i].phase == Phase.EO
        assert examples[i].raw_label == "EO"


def test_raw_label_carries_through(tmp_path):
    """Author labels survive JSONL round-trip."""
    seg = make_segmented()
    record = segmented_to_dict(seg)
    path = tmp_path / "test.jsonl"
    path.write_text(json.dumps(record) + "\n")
    examples = list(iter_examples_from_jsonl(path))
    assert len(examples) == seg.reconstruction.length
    # The "DR, 4a1" label should be on moves 5-9 (cumulative 10).
    assert examples[5].raw_label == "DR, 4a1"


def test_record_to_examples_matches_examples_from_segmented():
    """Loading via JSONL gives the same examples as direct segmenter."""
    seg = make_segmented()
    direct = examples_from_segmented(seg)
    record = segmented_to_dict(seg)
    via_record = record_to_examples(record)
    assert len(direct) == len(via_record)
    for a, b in zip(direct, via_record):
        assert a.source_id == b.source_id
        assert a.move_index == b.move_index
        assert a.target_move == b.target_move
        assert a.state_before == b.state_before
        assert a.phase == b.phase
        assert a.raw_label == b.raw_label
        assert a.method == b.method


def test_target_moves_form_full_solution(tmp_path):
    """Concatenated target_moves == flat solution."""
    seg = make_segmented()
    examples = examples_from_segmented(seg)
    targets = [ex.target_move for ex in examples]
    assert format_alg(targets) == format_alg(seg.reconstruction.solution.flat())
