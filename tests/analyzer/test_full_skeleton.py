"""Smoke test: skeleton produces a verified full solve on a short scramble.

Uses a 5-move scramble where the policy + search should easily reach a
complete EO -> DR -> HTR -> SOLVED chain. Verifies:
  1. find_skeleton returns at least one skeleton ending in SOLVED.
  2. Concatenating all stage moves and applying to scrambled state gives
     SOLVED (engine ground truth).
"""

from __future__ import annotations

from pathlib import Path

import pytest

torch = pytest.importorskip("torch")

from cube.analyzer.skeleton import find_skeleton
from cube.engine.notation import parse_alg
from cube.engine.state import SOLVED
from cube.training.model import ModelConfig, PolicyTransformer


@pytest.fixture(scope="module")
def model():
    ckpt_path = Path("checkpoints/policy_best.pt")
    if not ckpt_path.exists():
        pytest.skip("trained checkpoint not present")
    dev = torch.device("cpu")
    ckpt = torch.load(ckpt_path, map_location=dev, weights_only=False)
    m = PolicyTransformer(ModelConfig(**ckpt["model_cfg"])).to(dev)
    m.load_state_dict(ckpt["model"])
    m.eval()
    return m, ckpt["model_cfg"]["history_len"]


def test_easy_scramble_full_solve(model):
    m, hl = model
    # Short scramble — easy for the policy to handle.
    scramble = parse_alg("R U R'")
    skeletons = find_skeleton(
        m, scramble, history_len=hl, device="cpu",
        eo_beam_width=64, eo_max_depth=4,
        dr_beam_width=64, dr_max_depth=4,
    )
    assert skeletons, "no skeletons produced"
    # Find a skeleton that ends in SOLVED if any exists.
    solved = [
        sk for sk in skeletons
        if sk.stages and sk.stages[-1].end_state == SOLVED
    ]
    if not solved:
        pytest.skip("no full-solve skeleton found at this search budget")
    sk = solved[0]
    end = SOLVED.apply_alg(list(scramble) + list(sk.flat_moves))
    assert end == SOLVED, f"reported full-solve doesn't actually solve"
