#!/bin/bash
# =============================================================================
# GENESIS PLATFORM — Run All Verification Scripts
# =============================================================================
#
# This script executes all four verification scripts in sequence.
# Requirements: Python 3.x, numpy
#
# Usage:
#   chmod +x run_all_verifications.sh
#   ./run_all_verifications.sh
#
# =============================================================================

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

echo ""
echo "============================================================"
echo "  GENESIS PLATFORM — FULL VERIFICATION SUITE"
echo "============================================================"
echo ""
echo "  Running 4 verification scripts..."
echo "  Each loads real FEA data from EVIDENCE/ and performs"
echo "  independent analysis."
echo ""

# Track pass/fail
PASS=0
FAIL=0

# --- Script 1: Rectangle Failure ---
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  [1/4] verify_rectangle_failure.py"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
if python3 "$SCRIPT_DIR/verify_rectangle_failure.py"; then
    PASS=$((PASS + 1))
else
    FAIL=$((FAIL + 1))
fi

# --- Script 2: k_azi Sweep ---
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  [2/4] verify_kazi_sweep.py"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
if python3 "$SCRIPT_DIR/verify_kazi_sweep.py"; then
    PASS=$((PASS + 1))
else
    FAIL=$((FAIL + 1))
fi

# --- Script 3: Design-Around Analysis ---
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  [3/4] verify_design_desert.py"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
if python3 "$SCRIPT_DIR/verify_design_desert.py"; then
    PASS=$((PASS + 1))
else
    FAIL=$((FAIL + 1))
fi

# --- Script 4: Physics Computation ---
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  [4/4] compute_cartesian_stiffness.py"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
if python3 "$SCRIPT_DIR/compute_cartesian_stiffness.py"; then
    PASS=$((PASS + 1))
else
    FAIL=$((FAIL + 1))
fi

# --- Summary ---
echo ""
echo "============================================================"
echo "  VERIFICATION SUITE COMPLETE"
echo "============================================================"
echo ""
echo "  Passed: $PASS / $((PASS + FAIL))"
echo "  Failed: $FAIL / $((PASS + FAIL))"
echo ""

if [ $FAIL -eq 0 ]; then
    echo "  ✅ ALL VERIFICATIONS PASSED"
else
    echo "  ❌ SOME VERIFICATIONS FAILED — Review output above"
fi

echo ""
echo "============================================================"
echo ""
