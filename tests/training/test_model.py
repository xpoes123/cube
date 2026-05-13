"""Smoke tests for the policy transformer + torch dataset.

These are intentionally tiny — full quality is verified by the training
metrics on the actual corpus, not unit tests.
"""

from __future__ import annotations

import pytest

torch = pytest.importorskip("torch")

from cube.engine.moves import Face, Move, Turn
from cube.engine.state import SOLVED
from cube.segmenter.types import Method
from cube.training.dataset import TrainingExample
from cube.training.model import (
    PAD_MOVE,
    ModelConfig,
    PolicyTransformer,
    count_params,
)
from cube.training.torchdata import _examples_to_bundle


def _example(prev_moves: tuple[Move, ...], target: Move) -> TrainingExample:
    state = SOLVED
    for m in prev_moves:
        state = state.apply(m)
    return TrainingExample(
        source_id="test",
        move_index=len(prev_moves),
        state_before=state,
        target_move=target,
        history=prev_moves,
        phase=None,
        raw_label=None,
        method=Method.UNKNOWN,
    )


def test_forward_shape():
    cfg = ModelConfig(d_model=32, n_layers=1, n_heads=2, history_len=8)
    model = PolicyTransformer(cfg)

    examples = [
        _example((), Move(Face.U, Turn.CW)),
        _example((Move(Face.R, Turn.CW),), Move(Face.U, Turn.CW)),
    ]
    bundle = _examples_to_bundle(examples, history_len=cfg.history_len)
    out = model(
        bundle.cp.long(), bundle.co.long(), bundle.ep.long(),
        bundle.eo.long(), bundle.eo_fb.long(), bundle.eo_rl.long(),
        bundle.history.long(),
    )
    assert out.shape == (2, 18)


def test_history_padding():
    cfg = ModelConfig(history_len=8)
    examples = [_example((Move(Face.R, Turn.CW),), Move(Face.U, Turn.CW))]
    bundle = _examples_to_bundle(examples, history_len=cfg.history_len)
    # 7 PAD slots then 1 real move (encoded R = face 2 * 3 + 0 = 6).
    assert bundle.history.shape == (1, 8)
    assert int(bundle.history[0, -1].item()) == 6
    for i in range(7):
        assert int(bundle.history[0, i].item()) == PAD_MOVE


def test_one_step_reduces_loss():
    """Train one step on a single-batch synthetic problem; loss should drop."""
    torch.manual_seed(0)
    cfg = ModelConfig(d_model=32, n_layers=1, n_heads=2, history_len=8)
    model = PolicyTransformer(cfg)
    examples = [
        _example((), Move(Face.U, Turn.CW)),
        _example((Move(Face.R, Turn.CW),), Move(Face.F, Turn.CW)),
        _example((Move(Face.U, Turn.CW), Move(Face.F, Turn.HALF)), Move(Face.D, Turn.CCW)),
    ]
    bundle = _examples_to_bundle(examples, history_len=cfg.history_len)

    optim = torch.optim.AdamW(model.parameters(), lr=1e-2)
    loss_fn = torch.nn.CrossEntropyLoss()

    def step():
        logits = model(
            bundle.cp.long(), bundle.co.long(), bundle.ep.long(),
            bundle.eo.long(), bundle.eo_fb.long(), bundle.eo_rl.long(),
            bundle.history.long(),
        )
        return loss_fn(logits, bundle.target)

    initial = step().item()
    for _ in range(20):
        optim.zero_grad()
        loss = step()
        loss.backward()
        optim.step()
    final = step().item()
    assert final < initial * 0.5


def test_param_count_sane():
    cfg = ModelConfig()
    model = PolicyTransformer(cfg)
    n = count_params(model)
    # v0 target was 200-500k; keep a loose sanity band.
    assert 100_000 < n < 1_000_000
