#!/usr/bin/env python3
"""
REPRODUCIBILITY SCRIPT: Verify the chaos cliff phenomenon.

This script loads the k_azi dense sweep data and demonstrates the existence
of a "chaos cliff" between k_azi 0.7-1.15 where warpage variance explodes.

The physics: There are two stable operating regions (sweet spots A and B).
Between them lies an unstable transition zone where small k_azi changes
produce large, unpredictable warpage variations.

Run: python verify_chaos_cliff.py
"""

import json
import os
from pathlib import Path
from collections import defaultdict
import math

# -----------------------------------------------------------------------------
# CONFIGURATION
# -----------------------------------------------------------------------------
EVIDENCE_DIR = Path(__file__).parent.parent / "EVIDENCE"
KAZI_FILE = EVIDENCE_DIR / "kazi_dense_sweep.json"

# Operating regions (from design_around_impossibility.json)
SWEET_SPOT_A = (0.0, 0.5)
TRANSITION_1 = (0.5, 0.7)
CHAOS_CLIFF = (0.7, 1.15)
SWEET_SPOT_B = (1.15, 1.6)

# -----------------------------------------------------------------------------
# STATISTICS
# -----------------------------------------------------------------------------
def mean(values):
    return sum(values) / len(values) if values else 0

def std_dev(values):
    if len(values) < 2:
        return 0
    m = mean(values)
    variance = sum((x - m) ** 2 for x in values) / (len(values) - 1)
    return math.sqrt(variance)

def cv_percent(values):
    """Coefficient of variation as percentage."""
    m = mean(values)
    if m == 0:
        return 0
    return 100 * std_dev(values) / m

# -----------------------------------------------------------------------------
# VERIFICATION LOGIC
# -----------------------------------------------------------------------------
def load_kazi_data():
    """Load the k_azi sweep data."""
    with open(KAZI_FILE, 'r') as f:
        data = json.load(f)
    return data

def classify_region(k_azi):
    """Classify which operating region a k_azi value falls into."""
    if k_azi <= SWEET_SPOT_A[1]:
        return "Sweet Spot A"
    elif k_azi <= TRANSITION_1[1]:
        return "Transition"
    elif k_azi <= CHAOS_CLIFF[1]:
        return "CHAOS CLIFF"
    elif k_azi <= SWEET_SPOT_B[1]:
        return "Sweet Spot B"
    else:
        return "Beyond B"

def analyze_chaos_cliff(data):
    """
    Analyze the k_azi sweep to identify the chaos cliff.
    
    We group cases by operating region and compute the coefficient of
    variation (CV) for each. The chaos cliff should show significantly
    higher CV than the sweet spots.
    """
    # Group by region
    regions = defaultdict(list)
    
    for case in data:
        k_azi = case['k_azi']
        W_pv = case['W_pv_nm']
        region = classify_region(k_azi)
        regions[region].append({
            'k_azi': k_azi,
            'W_pv_nm': W_pv,
            'task_id': case.get('task_id', 'N/A')
        })
    
    print("=" * 70)
    print("VERIFICATION: Chaos Cliff at k_azi 0.7-1.15")
    print("=" * 70)
    print()
    
    # Display by k_azi order
    print("Individual measurements (sorted by k_azi):")
    print("-" * 70)
    for case in sorted(data, key=lambda x: x['k_azi']):
        region = classify_region(case['k_azi'])
        marker = "⚠️ " if region == "CHAOS CLIFF" else "  "
        print(f"{marker}k_azi={case['k_azi']:.2f} → W_pv={case['W_pv_nm']:.1f} nm  [{region}]")
    print()
    
    # Statistics by region
    print("Statistics by Operating Region:")
    print("-" * 70)
    print(f"{'Region':<20} {'Cases':>6} {'Mean W_pv':>12} {'Std Dev':>10} {'CV %':>8}")
    print("-" * 70)
    
    chaos_cv = 0
    sweet_a_cv = 0
    sweet_b_cv = 0
    
    for region_name in ["Sweet Spot A", "Transition", "CHAOS CLIFF", "Sweet Spot B", "Beyond B"]:
        if region_name not in regions:
            continue
        cases = regions[region_name]
        warpage_values = [c['W_pv_nm'] for c in cases]
        
        m = mean(warpage_values)
        s = std_dev(warpage_values)
        cv = cv_percent(warpage_values)
        
        if region_name == "CHAOS CLIFF":
            chaos_cv = cv
            marker = "❌"
        elif region_name == "Sweet Spot A":
            sweet_a_cv = cv
            marker = "✅"
        elif region_name == "Sweet Spot B":
            sweet_b_cv = cv
            marker = "✅"
        else:
            marker = "  "
        
        print(f"{marker} {region_name:<18} {len(cases):>6} {m:>12.1f} {s:>10.1f} {cv:>8.1f}%")
    
    print("-" * 70)
    print()
    
    return chaos_cv, sweet_a_cv, sweet_b_cv

def main():
    print()
    print("╔══════════════════════════════════════════════════════════════════════╗")
    print("║  GENESIS PLATFORM — REPRODUCIBILITY VERIFICATION                    ║")
    print("║  Patent Claim: Chaos cliff exists at k_azi 0.7-1.15                  ║")
    print("╚══════════════════════════════════════════════════════════════════════╝")
    print()
    
    # Load data
    data = load_kazi_data()
    print(f"Loaded {len(data)} FEA cases from: {KAZI_FILE.name}")
    print()
    
    # Analyze
    chaos_cv, sweet_a_cv, sweet_b_cv = analyze_chaos_cliff(data)
    
    # Verdict
    print("=" * 70)
    avg_sweet_cv = (sweet_a_cv + sweet_b_cv) / 2 if sweet_b_cv > 0 else sweet_a_cv
    
    if chaos_cv > avg_sweet_cv * 1.5:  # Cliff should have at least 1.5x higher CV
        ratio = chaos_cv / avg_sweet_cv if avg_sweet_cv > 0 else float('inf')
        print(f"✅ VERIFIED: Chaos cliff shows {ratio:.1f}x higher variance than sweet spots.")
        print()
        print("   This confirms the patent claim that operating at k_azi 0.7-1.15")
        print("   produces unstable, unpredictable warpage behavior.")
        print()
        print("   Competitors operating in this range will experience:")
        print("   - High manufacturing variance")
        print("   - Unpredictable yield losses")
        print("   - Inability to meet tight specifications")
    else:
        print("⚠️  Chaos cliff not clearly demonstrated in this dataset.")
        print(f"   Cliff CV: {chaos_cv:.1f}%, Sweet spot avg CV: {avg_sweet_cv:.1f}%")
    print("=" * 70)
    print()

if __name__ == "__main__":
    main()
