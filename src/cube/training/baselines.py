"""Non-ML baselines for next-move prediction.

These are deliberately stupid models that don't use cube state at all — just
counts. They give us a benchmark accuracy that the eventual ML model must
beat handily, plus they validate the data pipeline end-to-end.

- FrequencyBaseline: P(move) — predict the global most-common move.
- PhaseFrequencyBaseline: P(move | phase) — most-common move per phase.
- BigramBaseline: P(move | prev_move) — most-common move given prior move.
- BigramPhaseBaseline: P(move | prev_move, phase) — bigram conditioned on phase.

All baselines fit by counting, predict by argmax, and report accuracy.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from collections.abc import Iterable

from cube.engine.moves import Move
from cube.segmenter.types import Phase
from cube.training.dataset import TrainingExample
from cube.training.encoding import decode_move, encode_move


class FrequencyBaseline:
    """P(move) — ignores everything, predicts the global most common move."""

    def __init__(self) -> None:
        self.counts: Counter[int] = Counter()
        self.global_top: int = 0

    def fit(self, examples: Iterable[TrainingExample]) -> None:
        for ex in examples:
            self.counts[encode_move(ex.target_move)] += 1
        if self.counts:
            self.global_top = self.counts.most_common(1)[0][0]

    def predict(self, example: TrainingExample) -> Move:
        return decode_move(self.global_top)


class PhaseFrequencyBaseline:
    """P(move | phase) — most common move per phase, fallback to global."""

    def __init__(self) -> None:
        self.counts: dict[Phase | None, Counter[int]] = defaultdict(Counter)
        self.global_counts: Counter[int] = Counter()
        self.global_top: int = 0

    def fit(self, examples: Iterable[TrainingExample]) -> None:
        for ex in examples:
            move_idx = encode_move(ex.target_move)
            self.counts[ex.phase][move_idx] += 1
            self.global_counts[move_idx] += 1
        if self.global_counts:
            self.global_top = self.global_counts.most_common(1)[0][0]

    def predict(self, example: TrainingExample) -> Move:
        counts = self.counts.get(example.phase)
        if counts:
            return decode_move(counts.most_common(1)[0][0])
        return decode_move(self.global_top)


class BigramBaseline:
    """P(move | prev_move) — first-order Markov over moves."""

    _START = -1  # sentinel for "no previous move"

    def __init__(self) -> None:
        self.counts: dict[int, Counter[int]] = defaultdict(Counter)
        self.global_counts: Counter[int] = Counter()
        self.global_top: int = 0

    def fit(self, examples: Iterable[TrainingExample]) -> None:
        for ex in examples:
            prev_idx = encode_move(ex.history[-1]) if ex.history else self._START
            move_idx = encode_move(ex.target_move)
            self.counts[prev_idx][move_idx] += 1
            self.global_counts[move_idx] += 1
        if self.global_counts:
            self.global_top = self.global_counts.most_common(1)[0][0]

    def predict(self, example: TrainingExample) -> Move:
        prev_idx = encode_move(example.history[-1]) if example.history else self._START
        counts = self.counts.get(prev_idx)
        if counts:
            return decode_move(counts.most_common(1)[0][0])
        return decode_move(self.global_top)


class BigramPhaseBaseline:
    """P(move | prev_move, phase) — bigram conditioned on phase."""

    _START = -1

    def __init__(self) -> None:
        self.counts: dict[tuple[int, Phase | None], Counter[int]] = defaultdict(Counter)
        self.phase_counts: dict[Phase | None, Counter[int]] = defaultdict(Counter)
        self.global_counts: Counter[int] = Counter()
        self.global_top: int = 0

    def fit(self, examples: Iterable[TrainingExample]) -> None:
        for ex in examples:
            prev_idx = encode_move(ex.history[-1]) if ex.history else self._START
            move_idx = encode_move(ex.target_move)
            self.counts[(prev_idx, ex.phase)][move_idx] += 1
            self.phase_counts[ex.phase][move_idx] += 1
            self.global_counts[move_idx] += 1
        if self.global_counts:
            self.global_top = self.global_counts.most_common(1)[0][0]

    def predict(self, example: TrainingExample) -> Move:
        prev_idx = encode_move(example.history[-1]) if example.history else self._START
        key = (prev_idx, example.phase)
        # Try most-specific → less specific.
        counts = self.counts.get(key)
        if counts:
            return decode_move(counts.most_common(1)[0][0])
        # Fall back to phase-only.
        counts = self.phase_counts.get(example.phase)
        if counts:
            return decode_move(counts.most_common(1)[0][0])
        return decode_move(self.global_top)


def accuracy(model, examples: list[TrainingExample]) -> float:
    """Top-1 accuracy on the given examples."""
    if not examples:
        return 0.0
    correct = sum(1 for ex in examples if model.predict(ex) == ex.target_move)
    return correct / len(examples)


def topk_accuracy_baseline(model, examples: list[TrainingExample], k: int = 5) -> float:
    """For baselines that expose `counts`, compute top-k accuracy.

    Top-k = predicting one of the k most likely moves. Useful for tree
    explorer scoring where you'd display multiple branches.
    """
    if not examples:
        return 0.0
    correct = 0
    for ex in examples:
        # Find the model's top-k for this example.
        if isinstance(model, FrequencyBaseline):
            top = [m for m, _ in model.counts.most_common(k)]
        elif isinstance(model, PhaseFrequencyBaseline):
            counts = model.counts.get(ex.phase) or model.global_counts
            top = [m for m, _ in counts.most_common(k)]
        elif isinstance(model, BigramBaseline):
            prev_idx = encode_move(ex.history[-1]) if ex.history else BigramBaseline._START
            counts = model.counts.get(prev_idx) or model.global_counts
            top = [m for m, _ in counts.most_common(k)]
        elif isinstance(model, BigramPhaseBaseline):
            prev_idx = encode_move(ex.history[-1]) if ex.history else BigramPhaseBaseline._START
            counts = (
                model.counts.get((prev_idx, ex.phase))
                or model.phase_counts.get(ex.phase)
                or model.global_counts
            )
            top = [m for m, _ in counts.most_common(k)]
        else:
            raise TypeError(f"unsupported model: {type(model).__name__}")
        if encode_move(ex.target_move) in top:
            correct += 1
    return correct / len(examples)
