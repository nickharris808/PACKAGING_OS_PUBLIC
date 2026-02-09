#!/bin/bash
# PACKAGING OS PUBLIC - Full Verification Suite (v2.0)
# All scripts run locally, no dependencies beyond Python 3 + json module
# Tests 7 independent claims across 500+ FEM cases

set -e

echo "============================================================"
echo "PACKAGING OS PUBLIC - FULL VERIFICATION SUITE v2.0"
echo "============================================================"
echo ""

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

echo "[1/7] Verifying: Rectangular substrate k_azi = 0%..."
python3 "$SCRIPT_DIR/verify_rectangle_failure.py"
echo ""

echo "[2/7] Verifying: k_azi sweep chaos cliff..."
python3 "$SCRIPT_DIR/verify_kazi_sweep.py"
echo ""

echo "[3/7] Verifying: Design-around impossibility..."
python3 "$SCRIPT_DIR/verify_design_desert.py"
echo ""

echo "[4/7] Computing: Cartesian stiffness from first principles..."
python3 "$SCRIPT_DIR/compute_cartesian_stiffness.py"
echo ""

echo "[5/7] Verifying: Multi-die scaling crisis (3/5/8 HBM)..."
python3 "$SCRIPT_DIR/verify_multi_die_scaling.py"
echo ""

echo "[6/7] Verifying: Fatigue life (10B+ cycles all interfaces)..."
python3 "$SCRIPT_DIR/verify_fatigue_life.py"
echo ""

echo "[7/7] Verifying: Material invariance (InP, GaN, AlN cliff)..."
python3 "$SCRIPT_DIR/verify_material_invariance.py"
echo ""

echo "============================================================"
echo "ALL 7 VERIFICATIONS PASSED"
echo "============================================================"
echo ""
echo "Evidence verified:"
echo "  - 30 rectangular substrate cases (0% k_azi effect)"
echo "  - 41 k_azi sweep cases (chaos cliff confirmed)"
echo "  - 237 design-around cases (all paths blocked)"
echo "  - 192 multi-die cases (0% pass at 3/5/8 HBM)"
echo "  - 4 fatigue interfaces (all >10 billion cycles)"
echo "  - 15 material sweep cases (cliff in InP, GaN, AlN)"
echo "  Total: 500+ independently verified FEM cases"