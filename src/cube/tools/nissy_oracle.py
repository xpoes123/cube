"""Nissy subprocess wrapper — the FMC optimal-move oracle.

Wraps Tronto's `nissy` binary to query optimal-length solutions for
each FMC step. Returns parsed (moves, length) tuples and optimal-move
distributions for training the brain.

Nissy step → our model mapping:
    eoud      → EO model (canonical UD axis)
    drud      → DR model (after eoud is applied to scramble)
    htr-drud  → HTR model (after drud is applied; need DR on UD)
    htrfin    → Finish model (after htr is applied)

Pipeline shape (state is implicit in the move-history-appended scramble):

    scramble                       --eoud→     eo_moves
    scramble + eo_moves            --drud→     dr_moves
    scramble + eo + dr             --htr-drud→ htr_moves
    scramble + eo + dr + htr       --htrfin→   finish_moves

Each step gives us a (state_before_step, optimal_first_move_distribution)
training datum. The optimal-move distribution comes from enumerating
N optimal solutions and counting how often each first-move appears.
"""

from __future__ import annotations

import shutil
import subprocess
from dataclasses import dataclass


_NISSY_BIN: str | None = None


def nissy_path() -> str:
    """Locate the nissy binary (cached). Raises if not on PATH."""
    global _NISSY_BIN
    if _NISSY_BIN is None:
        found = shutil.which("nissy")
        if not found:
            raise RuntimeError("nissy binary not found on PATH")
        _NISSY_BIN = found
    return _NISSY_BIN


@dataclass(frozen=True, slots=True)
class NissyResult:
    """One nissy invocation's output."""

    step: str
    scramble: list[str]
    solutions: list[list[str]]  # each is a move list
    optimal_length: int  # length of the shortest solution returned

    @property
    def first_move_distribution(self) -> dict[str, float]:
        """P(move | state) computed from first-moves of optimal solutions.

        If multiple equally-optimal solutions exist, each first-move gets
        weight proportional to how often it appears.
        """
        if not self.solutions:
            return {}
        counts: dict[str, int] = {}
        n = 0
        for sol in self.solutions:
            if not sol:
                # 0-move solution means "already solved for this step"
                # We don't emit a distribution for already-solved states.
                continue
            counts[sol[0]] = counts.get(sol[0], 0) + 1
            n += 1
        if n == 0:
            return {}
        return {m: c / n for m, c in counts.items()}


def _parse_solutions(stdout: str) -> tuple[list[list[str]], int]:
    """Parse nissy's solve output. Returns (solutions, optimal_length).

    Output format (with -p flag for plain style):
        D R F' L' D
        D F' R L' D
        D' R B L D

    Without -p, each line ends with `(N)`. We always pass -p.
    """
    sols: list[list[str]] = []
    for line in stdout.splitlines():
        line = line.strip()
        if not line:
            continue
        # Filter out diagnostic lines like "Cube not ready for solving step: ..."
        if line.startswith("Cube not ready") or line.startswith("Error"):
            continue
        moves = line.split()
        sols.append(moves)
    if not sols:
        return [], 0
    opt = min(len(s) for s in sols)
    return sols, opt


def solve_step(
    step: str,
    scramble: list[str],
    *,
    n_solutions: int = 50,
    timeout_s: float = 60.0,
) -> NissyResult:
    """Solve one step from the given scramble. Returns up to n_solutions
    optimal-length solutions (when n_solutions > 1, the `-o -n N` flags
    enumerate all optimal solutions up to N).

    Args:
        step: nissy step name, e.g. 'eoud', 'drud', 'htr-drud', 'htrfin'.
        scramble: the scramble + any prior step moves, as a flat list.
        n_solutions: cap on how many optimal solutions to enumerate.
        timeout_s: subprocess timeout.

    Returns:
        NissyResult with the parsed solutions and helpers.
    """
    cmd = [nissy_path(), "solve", step, "-o", "-n", str(n_solutions), "-p",
           " ".join(scramble)]
    proc = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout_s)
    if proc.returncode != 0:
        # Nissy uses returncode 0 even on "Cube not ready" — true errors set non-zero.
        raise RuntimeError(f"nissy failed (rc={proc.returncode}): {proc.stderr.strip()}")
    solutions, optimal_length = _parse_solutions(proc.stdout)
    return NissyResult(
        step=step,
        scramble=list(scramble),
        solutions=solutions,
        optimal_length=optimal_length,
    )


# ---------------------------------------------------------------------------
# High-level pipeline composer
# ---------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class StepDatum:
    """A single (state, optimal-move-distribution) training datum."""

    step_name: str  # 'eo', 'dr', 'htr', 'finish'
    # Moves applied to SOLVED to reach the state BEFORE this step.
    # Empty for the EO step (state is just the scramble applied to SOLVED).
    prior_moves: list[str]
    # The scramble itself (state = SOLVED.apply(scramble + prior_moves))
    scramble: list[str]
    # P(first_move | state)
    move_distribution: dict[str, float]
    # The optimal solution chosen for the cascade (first one nissy returned).
    chosen_optimal: list[str]
    # Length of the optimal solution.
    optimal_length: int


def full_pipeline(
    scramble: list[str], *, n_solutions: int = 50, timeout_s: float = 60.0,
) -> list[StepDatum]:
    """Walk a scramble through eoud → drud → htr-drud → htrfin via nissy,
    capturing the (state, optimal-move-distribution) datum at EACH step.

    Returns 4 StepDatum (or fewer if some step is already solved). The
    chosen_optimal for each step is appended to prior_moves before the
    next step query — this gives us the cascaded state.

    Note: this only captures the TOP-LEVEL state per step (the state at
    the moment the step starts). For richer training data, `gen_training_data.py`
    will additionally unroll each step's optimal solution to extract
    every intermediate (state, optimal_move) pair.
    """
    out: list[StepDatum] = []
    pipeline = [
        ("eo", "eoud"),
        ("dr", "drud"),
        ("htr", "htr-drud"),
        ("finish", "htrfin"),
    ]
    cumulative: list[str] = []
    for step_name, nissy_step in pipeline:
        # Pass scramble + cumulative-prior-step-moves to nissy.
        full_input = list(scramble) + list(cumulative)
        try:
            res = solve_step(nissy_step, full_input,
                             n_solutions=n_solutions, timeout_s=timeout_s)
        except RuntimeError:
            break  # nissy step failed, end of pipeline
        if not res.solutions:
            break  # no solution → upstream state not ready
        chosen = list(res.solutions[0])
        out.append(StepDatum(
            step_name=step_name,
            prior_moves=list(cumulative),
            scramble=list(scramble),
            move_distribution=res.first_move_distribution,
            chosen_optimal=chosen,
            optimal_length=res.optimal_length,
        ))
        cumulative.extend(chosen)
    return out
