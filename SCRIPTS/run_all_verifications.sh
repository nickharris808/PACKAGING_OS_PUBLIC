#!/bin/bash
#
# REPRODUCIBILITY SUITE — Run all verification scripts
#
# This script runs all verification checks to prove the patent claims.
# Scripts 1-3 parse real FEA data. Script 4 computes physics from first principles.
#
# Usage: ./run_all_verifications.sh
#

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo ""
echo "╔══════════════════════════════════════════════════════════════════════╗"
echo "║            GENESIS PLATFORM — FULL VERIFICATION SUITE                ║"
echo "║                                                                       ║"
echo "║  4 verifications: 3 data-driven + 1 physics computation              ║"
echo "╚══════════════════════════════════════════════════════════════════════╝"
echo ""

echo "Running verification 1/4: Rectangle Failure (30 FEA cases)..."
echo "─────────────────────────────────────────────────────────────────────────"
python3 "$SCRIPT_DIR/verify_rectangle_failure.py"

echo ""
echo "Running verification 2/4: Chaos Cliff (41 FEA cases)..."
echo "─────────────────────────────────────────────────────────────────────────"
python3 "$SCRIPT_DIR/verify_chaos_cliff.py"

echo ""
echo "Running verification 3/4: Design Desert (237 FEA cases)..."
echo "─────────────────────────────────────────────────────────────────────────"
python3 "$SCRIPT_DIR/verify_design_desert.py"

echo ""
echo "Running verification 4/4: Cartesian Stiffness (Physics Computation)..."
echo "─────────────────────────────────────────────────────────────────────────"
python3 "$SCRIPT_DIR/compute_cartesian_stiffness.py"

echo ""
echo "╔══════════════════════════════════════════════════════════════════════╗"
echo "║                     ALL VERIFICATIONS COMPLETE                       ║"
echo "╚══════════════════════════════════════════════════════════════════════╝"
echo ""
echo "Summary:"
echo "  ✅ [1/4] k_azi has no effect on rectangular substrates (30 FEA cases)"
echo "  ✅ [2/4] Chaos cliff exists at k_azi 0.7-1.15 (41 FEA cases)"
echo "  ✅ [3/4] All design-around paths are blocked (237 FEA cases)"
echo "  ✅ [4/4] Cartesian Stiffness computed from Kirchhoff-Love theory"
echo ""
echo "Total FEA cases verified: 308"
echo "All data traces to auditable Inductiva Cloud HPC task IDs."
echo ""
echo "This repository proves the PROBLEM. The SOLUTION is available under NDA."
echo ""
