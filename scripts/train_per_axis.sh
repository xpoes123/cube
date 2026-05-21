#!/bin/bash
# v35: per-axis brain retraining.
#
# Generates 300K scrambles of training data per DR axis (UD/FB/RL),
# then trains a brain model per (step, axis) — 12 checkpoints total
# (brain_eo_UD.pt, brain_eo_FB.pt, ..., brain_finish_RL.pt).
#
# Outputs:
#   data/brain_training/{step}_{axis}.jsonl
#   checkpoints/brain_{step}_{axis}.pt
#   runs/train_per_axis.log  (this script's stdout + stderr)
#
# Estimated wall time: ~32h data gen + ~6h training = ~38h end-to-end.

set -euo pipefail
cd "$(dirname "$0")/.."

LOG_DIR="runs"
mkdir -p "$LOG_DIR"
LOG="$LOG_DIR/train_per_axis.log"

N_SCRAMBLES=300000
WORKERS=12
EPOCHS=30

source .venv/bin/activate

echo "=== v35 per-axis brain retraining ===" | tee -a "$LOG"
echo "started: $(date)" | tee -a "$LOG"
echo "n_scrambles per axis: $N_SCRAMBLES" | tee -a "$LOG"
echo "workers: $WORKERS, training epochs: $EPOCHS" | tee -a "$LOG"

# ------------------------------------------------------------
# Phase 1: data generation, per axis
# ------------------------------------------------------------
for AXIS in UD FB RL; do
  echo | tee -a "$LOG"
  echo "[phase1] gen_training_data --axis $AXIS --n $N_SCRAMBLES" | tee -a "$LOG"
  echo "  start: $(date)" | tee -a "$LOG"
  python -m cube.brain.gen_training_data \
    --n $N_SCRAMBLES \
    --workers $WORKERS \
    --axis $AXIS \
    --out data/brain_training \
    2>&1 | tee -a "$LOG"
  echo "  done:  $(date)" | tee -a "$LOG"
done

# ------------------------------------------------------------
# Phase 2: train one model per (step, axis) — 12 in total.
# ------------------------------------------------------------
for AXIS in UD FB RL; do
  for STEP in eo dr htr finish; do
    echo | tee -a "$LOG"
    echo "[phase2] train.py --axis $AXIS --step $STEP" | tee -a "$LOG"
    echo "  start: $(date)" | tee -a "$LOG"
    python -m cube.brain.train \
      --axis $AXIS \
      --step $STEP \
      --epochs $EPOCHS \
      2>&1 | tee -a "$LOG"
    echo "  done:  $(date)" | tee -a "$LOG"
  done
done

echo | tee -a "$LOG"
echo "=== ALL DONE: $(date) ===" | tee -a "$LOG"
ls -la checkpoints/brain_*.pt | tee -a "$LOG"
