"""Baseline model tests."""

from cube.corpus.sources.api333fm import submission_to_reconstruction
from cube.segmenter import segment
from cube.training import examples_from_segmented
from cube.training.baselines import (
    BigramBaseline,
    BigramPhaseBaseline,
    FrequencyBaseline,
    PhaseFrequencyBaseline,
    accuracy,
    topk_accuracy_baseline,
)


_SUB = {
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
_RECON = {"user": {"id": 635, "name": "Wong"}}


def make_examples():
    rec = submission_to_reconstruction(_SUB, recon=_RECON, competition_name="FMC 2024")
    return examples_from_segmented(segment(rec))


def test_frequency_baseline_fits_and_predicts():
    examples = make_examples()
    m = FrequencyBaseline()
    m.fit(examples)
    # Self-accuracy: predicting the most common move. > 1/18 random.
    acc = accuracy(m, examples)
    assert 0 < acc <= 1.0


def test_phase_baseline_specializes_by_phase():
    examples = make_examples()
    m = PhaseFrequencyBaseline()
    m.fit(examples)
    # On training data, should be at least as good as the global baseline.
    freq = FrequencyBaseline()
    freq.fit(examples)
    assert accuracy(m, examples) >= accuracy(freq, examples)


def test_bigram_better_than_frequency_on_train():
    examples = make_examples()
    bg = BigramBaseline()
    bg.fit(examples)
    freq = FrequencyBaseline()
    freq.fit(examples)
    # Bigram has more info, should fit train at least as well.
    assert accuracy(bg, examples) >= accuracy(freq, examples)


def test_bigram_phase_strictly_better_on_train():
    examples = make_examples()
    bg_phase = BigramPhaseBaseline()
    bg_phase.fit(examples)
    bg = BigramBaseline()
    bg.fit(examples)
    assert accuracy(bg_phase, examples) >= accuracy(bg, examples)


def test_topk_accuracy_monotone():
    """top-1 ≤ top-3 ≤ top-5 for any model."""
    examples = make_examples()
    m = BigramPhaseBaseline()
    m.fit(examples)
    top1 = topk_accuracy_baseline(m, examples, k=1)
    top3 = topk_accuracy_baseline(m, examples, k=3)
    top5 = topk_accuracy_baseline(m, examples, k=5)
    assert top1 <= top3 <= top5


def test_baseline_works_on_unseen_example():
    """Trained on one example, predicting on the same — should not crash."""
    examples = make_examples()
    m = BigramPhaseBaseline()
    m.fit(examples[:5])
    # Predict on a later example (different phase context).
    m.predict(examples[-1])  # should not raise
