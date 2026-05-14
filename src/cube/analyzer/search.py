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

import heapq
from collections.abc import Callable
from dataclasses import dataclass, field

import torch
import torch.nn.functional as F

from cube.engine.moves import Move
from cube.engine.state import SOLVED, State
from cube.training.encoding import decode_move, encode_move
from cube.training.model import PAD_MOVE, N_MOVES, PolicyTransformer

# A predicate identifies a target state (EO, DR, SOLVED, block solved, …).
StatePredicate = Callable[[State], bool]

# An admissible heuristic: lower bound on moves-to-target from a state.
StateHeuristic = Callable[[State], int]


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
    extra_depths_after_first_hit: int = 0,
) -> list[Solution]:
    """Beam-search from `start_state` to any state where `target_predicate` is True.

    `seed_history` is the move sequence already played before `start_state`
    (e.g., scramble + prior stage's moves). It's only used to seed the
    model's history conditioning; it's NOT prepended to returned solutions.

    `allowed_move_indices` optionally restricts the action space (e.g., to
    EO-preserving moves during a DR stage). When None, all 18 moves are
    available.

    `extra_depths_after_first_hit`: when > 0, the search continues this
    many depths past the first hit-producing depth. Lets the caller collect
    longer-but-still-acceptable candidates (e.g. DR shortlist Δ=3 to find
    a longer DR with a better HTR subset). Overrides stop_at_first_hit.

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
    first_hit_depth: int | None = None

    for depth_idx in range(max_depth):
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

        if hits and first_hit_depth is None:
            first_hit_depth = depth_idx + 1
        if hits and stop_at_first_hit and extra_depths_after_first_hit == 0:
            return sorted(hits, key=lambda s: s.log_prob, reverse=True)
        if (
            first_hit_depth is not None
            and depth_idx + 1 >= first_hit_depth + extra_depths_after_first_hit
        ):
            return sorted(hits, key=lambda s: (len(s), -s.log_prob))

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


# =====================================================================
# A* search
# =====================================================================
#
# Beam is policy-blind to "am I closer to the target." A* fixes that by
# expanding nodes in order of f(n) = g(n) + h(n), where:
#   g(n) = path cost (depth so far)
#   h(n) = admissible lower bound on remaining moves to target
# With an admissible h, A* is guaranteed optimal.
#
# We add a third term, policy_bias = -lambda * log_p(path), so f becomes:
#   f(n) = g(n) + h(n) - lambda * log_p(path)
# When lambda = 0, A* finds the optimal-length sequence. When lambda > 0,
# it prefers higher-policy-probability paths among ties — sacrificing
# some optimality for human-style move ordering. This is the same idea
# AlphaZero uses with a learned value, just with a hand-coded h.

# Sentinel returned by the policy when policy_weight is 0 (skip forwards).
_NO_POLICY = None


@dataclass(order=True)
class _AStarNode:
    f: float
    counter: int                      # tiebreaker for the heap (state-comparison-free)
    state: State = field(compare=False)
    history: tuple[Move, ...] = field(compare=False)
    g: int = field(compare=False)
    log_prob: float = field(compare=False)


def _policy_log_probs_batched(
    model: PolicyTransformer,
    states: list[State],
    histories: list[tuple[Move, ...]],
    history_len: int,
    device: torch.device,
) -> list[list[float]]:
    """Run the model on a list of (state, history) pairs and return log-probs."""
    beams = [
        Beam(state=s, history=h, log_prob=0.0)
        for s, h in zip(states, histories, strict=True)
    ]
    batch = _encode_beams(beams, history_len, device)
    with torch.no_grad():
        logits = model(**batch)
    return F.log_softmax(logits, dim=-1).cpu().tolist()


def a_star_search(
    model: PolicyTransformer | None,
    start_state: State,
    target_predicate: StatePredicate,
    heuristic: StateHeuristic,
    max_depth: int = 16,
    max_nodes: int = 100_000,
    history_len: int = 32,
    device: torch.device | str = "cuda",
    seed_history: tuple[Move, ...] = (),
    allowed_move_indices: tuple[int, ...] | None = None,
    policy_weight: float = 0.0,
    expansion_batch: int = 256,
) -> list[Solution]:
    """A* search from start_state to any state satisfying target_predicate.

    `heuristic(state)` must return an admissible lower bound on moves to target.

    `policy_weight` (lambda): when > 0 and `model` is provided, paths with
    higher policy log-prob are preferred among ties. Set to 0 for pure
    optimal-length search; set high to bias toward human-style moves.

    `max_nodes`: cap on the closed set size — safety valve for memory.

    Returns solutions sorted by length, then by policy log_prob (descending).
    Returns up to one solution per distinct path length found before depth
    or node limit is hit.
    """
    dev = torch.device(device) if isinstance(device, str) else device
    if model is not None:
        model.eval()

    move_iter = (
        tuple(range(N_MOVES))
        if allowed_move_indices is None
        else allowed_move_indices
    )

    if target_predicate(start_state):
        return [Solution(moves=(), log_prob=0.0)]

    counter = 0
    h0 = heuristic(start_state)
    start_node = _AStarNode(
        f=float(h0),
        counter=counter,
        state=start_state,
        history=seed_history,
        g=0,
        log_prob=0.0,
    )
    open_heap: list[_AStarNode] = [start_node]
    best_g: dict[State, int] = {start_state: 0}
    hits: list[Solution] = []
    seen_path_lengths: set[int] = set()
    seed_len = len(seed_history)

    use_policy = (model is not None) and (policy_weight > 0.0)

    while open_heap and len(best_g) < max_nodes:
        # Pop a batch of nodes to expand at once — lets us batch the
        # policy network call. We pull up to `expansion_batch` nodes off
        # the heap, but only those whose g is still consistent with the
        # best-known g (no stale entries).
        batch_nodes: list[_AStarNode] = []
        while open_heap and len(batch_nodes) < expansion_batch:
            node = heapq.heappop(open_heap)
            if node.g != best_g.get(node.state, -1):
                continue  # stale; skip
            if node.g >= max_depth:
                continue
            batch_nodes.append(node)

        if not batch_nodes:
            break

        # Optionally compute policy log-probs for the whole batch in one go.
        if use_policy:
            log_probs_batch = _policy_log_probs_batched(
                model,
                [n.state for n in batch_nodes],
                [n.history for n in batch_nodes],
                history_len,
                dev,
            )
        else:
            log_probs_batch = [[0.0] * N_MOVES for _ in batch_nodes]

        for node, log_probs in zip(batch_nodes, log_probs_batch, strict=True):
            for move_idx in move_iter:
                move = decode_move(move_idx)
                child_state = node.state.apply(move)
                child_g = node.g + 1
                if child_g > max_depth:
                    continue
                prior_g = best_g.get(child_state)
                if prior_g is not None and prior_g <= child_g:
                    continue

                child_log_prob = node.log_prob + log_probs[move_idx]
                child_history = node.history + (move,)

                if target_predicate(child_state):
                    stage_moves = child_history[seed_len:]
                    if len(stage_moves) not in seen_path_lengths:
                        hits.append(Solution(stage_moves, child_log_prob))
                        seen_path_lengths.add(len(stage_moves))
                    continue

                best_g[child_state] = child_g
                child_h = heuristic(child_state)
                child_f = child_g + child_h - policy_weight * child_log_prob
                counter += 1
                heapq.heappush(
                    open_heap,
                    _AStarNode(
                        f=child_f,
                        counter=counter,
                        state=child_state,
                        history=child_history,
                        g=child_g,
                        log_prob=child_log_prob,
                    ),
                )

        # Early-exit: once we've found a solution, the heap's min g + h is
        # a lower bound on remaining path lengths (h admissible). We stop
        # when no shorter solution can still be reached. Note: cannot use
        # `f` here since with policy_weight > 0, f includes a policy term
        # that breaks the g + h <= length guarantee.
        if hits and open_heap:
            shortest = min(len(s) for s in hits)
            # The g+h on the heap is bounded below by the lowest-f node's
            # g+h. Stop if the heap's lowest g+h would already exceed
            # `shortest` even without policy bonus.
            min_node = open_heap[0]
            min_remaining = min_node.g + heuristic(min_node.state)
            if min_remaining >= shortest:
                break
        elif hits and not open_heap:
            break

    return sorted(hits, key=lambda s: (len(s), -s.log_prob))
