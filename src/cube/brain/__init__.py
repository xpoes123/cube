"""The cube brain — state-conditioned move predictor.

Replaces the legacy `tools/policy.py` sequence-prediction transformer.
The brain takes a cube state (cubie permutations + orientations) and
emits a probability distribution over the next move, conditioned on
which FMC step the agent is working: EO, DR, HTR, or finish.

Architecture: small transformer over 20 cubie tokens (8 corners +
12 edges), 4 step-specific output heads. Trained per-step on the
optimal-move distribution from nissy as oracle.

Per-step output alphabet:
- eo:     all 18 face moves
- dr:     14 EO-preserving moves (canonical UD axis)
- htr:    10 DR-preserving moves
- finish: 6 half-turn moves

Axis collapse: train one model per *kind* of step in a canonical-axis
frame (UD). At inference, rotate state into UD frame, predict, rotate
move back. See `canonical_axis.py`.
"""
