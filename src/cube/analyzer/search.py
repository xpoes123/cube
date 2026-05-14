"""Policy-guided beam search over cube states.

The trained policy gives a prior `P(move | state, history)`. Beam search
expands the top-K most likely partial sequences at each depth, deduping
by reached state. The cube engine verifies every output — any sequence
returned from this function is guaranteed to satisfy the target predicate.

Search is staged toward *structural milestones* (EO, DR, blocks) rather
than end-to-end SOLVED. This matches how modern FMC actually works: pure
policy beam can't find a 25-move solve in 18^25 space, but it can find
the 4-7 moves to EO, then the 8-12 moves to DR, etc. Each stage is short
enough for beam to handle, each has a clean engine-verifiable predicate.

Why beam search (vs. MCTS or A*):
- No value head yet, so no moves-to-target estimate. That rules out A*.
- MCTS without a value function is just policy rollouts with backtracking;
  beam is cleaner and produces top-K candidates per stage naturally.
- The eventual tree explorer wants exactly this: top-K branches per stage,
  all engine-verified.
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass

import torch
import torch.nn.functional as F

from cube.engine.moves import Move
from cube.engine.state import SOLVED, State
from cube.training.encoding import decode_move, encode_move
from cube.training.model import PAD_MOVE, N_MOVES, PolicyTransformer

# A predicate identifies a target state (EO, DR, SOLVED, block solved, …).
StatePredicate = Callable[[State], bool]


@dataclass(frozen=True, slots=True)
class Beam:
    state: State
    history: tuple[Move, ...]   # moves played from the scrambled state
    log_prob: float             # sum of log P(move_i | state_i) along history


@dataclass(frozen=True, slots=True)
class Solution:
    moves: tuple[Move, ...]
    log_prob: float

    def __len__(self) -> int:
        return len(self.moves)


def _encode_beams(
    beams: list[Beam],
    history_len: int,
    device: torch.device,
) -> dict[str, torch.Tensor]:
    """Stack beams into model-input tensors."""
    n = len(beams)
    cp = torch.empty((n, 8), dtype=torch.long, device=device)
    co = torch.empty((n, 8), dtype=torch.long, device=device)
    ep = torch.empty((n, 12), dtype=torch.long, device=device)
    eo = torch.empty((n, 12), dtype=torch.long, device=device)
    eo_fb = torch.empty((n, 12), dtype=torch.long, device=device)
    eo_rl = torch.empty((n, 12), dtype=torch.long, device=device)
    history = torch.full(
        (n, history_len), PAD_MOVE, dtype=torch.long, device=device,
    )

    for i, beam in enumerate(beams):
        s = beam.state
        cp[i] = torch.tensor(s.cp, dtype=torch.long, device=device)
        co[i] = torch.tensor(s.co, dtype=torch.long, device=device)
        ep[i] = torch.tensor(s.ep, dtype=torch.long, device=device)
        eo[i] = torch.tensor(s.eo, dtype=torch.long, device=device)
        eo_fb[i] = torch.tensor(s.eo_fb, dtype=torch.long, device=device)
        eo_rl[i] = torch.tensor(s.eo_rl, dtype=torch.long, device=device)
        recent = beam.history[-history_len:]
        for j, m in enumerate(recent):
            history[i, history_len - len(recent) + j] = encode_move(m)

    return {
        "cp": cp, "co": co, "ep": ep,
        "eo": eo, "eo_fb": eo_fb, "eo_rl": eo_rl,
        "history": history,
    }


def beam_search(
    model: PolicyTransformer,
    start_state: State,
    target_predicate: StatePredicate,
    beam_width: int = 128,
    max_depth: int = 15,
    history_len: int = 32,
    device: torch.device | str = "cuda",
    seed_history: tuple[Move, ...] = (),
    stop_at_first_hit: bool = True,
    allowed_move_indices: tuple[int, ...] | None = None,
) -> list[Solution]:
    """Beam-search from `start_state` to any state where `target_predicate` is True.

    `seed_history` is the move sequence already played before `start_state`
    (e.g., scramble + prior stage's moves). It's only used to seed the
    model's history conditioning; it's NOT prepended to returned solutions.

    `allowed_move_indices` optionally restricts the action space (e.g., to
    EO-preserving moves during a DR stage). When None, all 18 moves are
    available.

    Returns solutions sorted by log_prob (descending). If
    `stop_at_first_hit`, terminates at the first depth where the predicate
    fires — returns all hits found at that depth.

    Empty list if no hit within `max_depth`. Caller should retry with
    larger beam_width or max_depth.
    """
    dev = torch.device(device) if isinstance(device, str) else device
    model.eval()

    if target_predicate(start_state):
        return [Solution(moves=(), log_prob=0.0)]

    beams: list[Beam] = [Beam(state=start_state, history=seed_history, log_prob=0.0)]
    hits: list[Solution] = []
    seed_len = len(seed_history)
    move_iter = (
        tuple(range(N_MOVES))
        if allowed_move_indices is None
        else allowed_move_indices
    )

    for _depth in range(max_depth):
        if not beams:
            break

        batch = _encode_beams(beams, history_len, dev)
        with torch.no_grad():
            logits = model(**batch)
        log_probs = F.log_softmax(logits, dim=-1).cpu().numpy()  # (n_beams, 18)

        candidates: list[Beam] = []
        for i, beam in enumerate(beams):
            for move_idx in move_iter:
                move = decode_move(move_idx)
                child_state = beam.state.apply(move)
                child_log_prob = beam.log_prob + float(log_probs[i, move_idx])
                child_history = beam.history + (move,)
                if target_predicate(child_state):
                    # Return only the moves played in this stage (drop seed_history).
                    stage_moves = child_history[seed_len:]
                    hits.append(Solution(stage_moves, child_log_prob))
                else:
                    candidates.append(
                        Beam(child_state, child_history, child_log_prob)
                    )

        if hits and stop_at_first_hit:
            return sorted(hits, key=lambda s: s.log_prob, reverse=True)

        candidates.sort(key=lambda b: b.log_prob, reverse=True)
        seen: set[State] = set()
        next_beams: list[Beam] = []
        for c in candidates:
            if c.state in seen:
                continue
            seen.add(c.state)
            next_beams.append(c)
            if len(next_beams) >= beam_width:
                break
        beams = next_beams

    return sorted(hits, key=lambda s: s.log_prob, reverse=True)


def format_solution(solution: Solution) -> str:
    return " ".join(str(m) for m in solution.moves)
