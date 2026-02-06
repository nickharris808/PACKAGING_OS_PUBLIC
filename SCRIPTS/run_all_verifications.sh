#!/bin/bash
# PACKAGING OS PUBLIC - Verification Suite
# All scripts run locally, no dependencies beyond Python 3 + numpy

set -e

echo "============================================================"
echo "PACKAGING OS PUBLIC - RUNNING ALL VERIFICATIONS"
echo "============================================================"
echo ""

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

echo "[1/4] Verifying: Rectangular substrate k_azi = 0%..."
python3 "$SCRIPT_DIR/verify_rectangle_failure.py"
echo ""

echo "[2/4] Verifying: k_azi sweep chaos cliff..."
python3 "$SCRIPT_DIR/verify_kazi_sweep.py"
echo ""

echo "[3/4] Verifying: Design-around impossibility..."
python3 "$SCRIPT_DIR/verify_design_desert.py"
echo ""

echo "[4/4] Computing: Cartesian stiffness from first principles..."
python3 "$SCRIPT_DIR/compute_cartesian_stiffness.py"
echo ""

echo "============================================================"
echo "ALL 4 VERIFICATIONS PASSED"
echo "============================================================"
