#!/usr/bin/env python3
"""
REPRODUCIBILITY SCRIPT: Verify k_azi has no effect on rectangular substrates.

This script loads the FEA evidence and demonstrates that azimuthal stiffness
modulation (k_azi) produces ZERO change in warpage on rectangular geometries.

The physics is simple: rectangular panels have no hoop stress (σ_θθ = 0),
so any control law based on azimuthal variation is ineffective.

Run: python verify_rectangle_failure.py
"""

import json
import os
from pathlib import Path

# -----------------------------------------------------------------------------
# CONFIGURATION
# -----------------------------------------------------------------------------
EVIDENCE_DIR = Path(__file__).parent.parent / "EVIDENCE"
RECT_FILE = EVIDENCE_DIR / "rectangular_substrates_FINAL.json"

# -----------------------------------------------------------------------------
# VERIFICATION LOGIC
# -----------------------------------------------------------------------------
def load_rectangular_data():
    """Load the 30 FEA cases for rectangular substrates."""
    with open(RECT_FILE, 'r') as f:
        data = json.load(f)
    return data

def analyze_k_azi_effect(data):
    """
    Group cases by geometry and load type, then show k_azi has no effect.
    
    Key insight: For the same geometry and load, varying k_azi from 0.3 to 1.0
    produces IDENTICAL warpage values. This proves azimuthal control is useless
    on rectangles.
    """
    # Group by geometry and load
    groups = {}
    for case in data:
        # Handle both field naming conventions
        geometry = case.get('geometry') or case.get('panel', 'unknown')
        load_type = case.get('load_type') or case.get('load', 'unknown')
        key = (geometry, load_type)
        if key not in groups:
            groups[key] = []
        groups[key].append({
            'k_azi': case['k_azi'],
            'W_pv_nm': case['W_pv_nm'],
            'task_id': case.get('task_id', 'N/A')
        })
    
    print("=" * 70)
    print("VERIFICATION: k_azi Effect on Rectangular Substrates")
    print("=" * 70)
    print()
    
    all_zero_effect = True
    
    for (geometry, load_type), cases in sorted(groups.items()):
        print(f"Geometry: {geometry}, Load: {load_type}")
        print("-" * 50)
        
        # Get unique warpage values
        warpage_values = [c['W_pv_nm'] for c in cases]
        k_azi_values = [c['k_azi'] for c in cases]
        
        min_w = min(warpage_values)
        max_w = max(warpage_values)
        variation = max_w - min_w
        
        for c in sorted(cases, key=lambda x: x['k_azi']):
            print(f"  k_azi={c['k_azi']:.1f} → W_pv={c['W_pv_nm']:.2f} nm  [task: {c['task_id'][:12]}...]")
        
        # Check if variation is effectively zero (< 0.01 nm)
        if variation > 0.01:
            all_zero_effect = False
            print(f"  ⚠️  VARIATION DETECTED: {variation:.4f} nm")
        else:
            print(f"  ✓ Variation: {variation:.4f} nm (effectively ZERO)")
        print()
    
    return all_zero_effect

def main():
    print()
    print("╔══════════════════════════════════════════════════════════════════════╗")
    print("║  GENESIS PLATFORM — REPRODUCIBILITY VERIFICATION                    ║")
    print("║  Patent Claim: Azimuthal stiffness has no effect on rectangles      ║")
    print("╚══════════════════════════════════════════════════════════════════════╝")
    print()
    
    # Load data
    data = load_rectangular_data()
    print(f"Loaded {len(data)} FEA cases from: {RECT_FILE.name}")
    print()
    
    # Analyze
    zero_effect = analyze_k_azi_effect(data)
    
    # Verdict
    print("=" * 70)
    if zero_effect:
        print("✅ VERIFIED: k_azi produces ZERO effect on rectangular substrates.")
        print()
        print("   This confirms the patent claim that azimuthal stiffness modulation,")
        print("   which relies on hoop stress (σ_θθ), is ineffective on geometries")
        print("   that lack circumferential symmetry.")
        print()
        print("   Competitors using k_azi-based control on rectangular glass panels")
        print("   will see NO improvement in warpage control.")
    else:
        print("❌ UNEXPECTED: Some variation detected. Review data.")
    print("=" * 70)
    print()

if __name__ == "__main__":
    main()
