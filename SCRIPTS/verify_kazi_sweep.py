#!/usr/bin/env python3
"""
VERIFY: k_azi Sweep on Circular Substrates Shows Chaos Cliff

This script loads the real 41-case dense k_azi sweep (circular glass substrate)
and verifies that warpage rises with k_azi, with a chaos cliff at 0.7-1.15.

Data source: kazi_dense_sweep.json (Inductiva Cloud HPC, CalculiX)
"""

import json
import os
import sys
import numpy as np

def main():
    print("="*60)
    print("VERIFICATION: k_azi Sweep Shows Chaos Cliff on Circular Glass")
    print("="*60)
    
    data_path = os.path.join(os.path.dirname(__file__), "..", "EVIDENCE", "kazi_dense_sweep.json")
    with open(data_path) as f:
        cases = json.load(f)
    
    print(f"\nLoaded {len(cases)} FEA cases (circular glass substrate)")
    print(f"All cases have Inductiva task_id: {all('task_id' in c for c in cases)}")
    
    k_azi = np.array([c['k_azi'] for c in cases])
    warpage = np.array([c['W_pv_nm'] for c in cases])
    
    print(f"\nk_azi range: {k_azi.min():.2f} - {k_azi.max():.2f}")
    print(f"Warpage range: {warpage.min():.1f} - {warpage.max():.1f} nm")
    
    # Check 1: Warpage at k_azi=0 (baseline)
    baseline = warpage[k_azi == 0.0]
    print(f"\nBaseline (k_azi=0): {baseline[0]:.1f} nm")
    
    # Check 2: Warpage generally rises with k_azi (trend)
    # Use linear regression to check overall trend
    from numpy.polynomial import polynomial as P
    coeffs = np.polyfit(k_azi, warpage, 1)
    slope = coeffs[0]
    print(f"Overall trend slope: {slope:.1f} nm per unit k_azi {'(RISING)' if slope > 0 else '(FALLING)'}")
    
    # Check 3: Chaos cliff region (k_azi 0.7-1.15)
    cliff_mask = (k_azi >= 0.7) & (k_azi <= 1.15)
    sweet_A_mask = k_azi <= 0.5
    
    cliff_warpages = warpage[cliff_mask]
    sweet_A_warpages = warpage[sweet_A_mask]
    
    cliff_cv = np.std(cliff_warpages) / np.mean(cliff_warpages) * 100
    sweet_cv = np.std(sweet_A_warpages) / np.mean(sweet_A_warpages) * 100
    
    print(f"\nSweet Spot A (k_azi 0-0.5):")
    print(f"  Mean warpage: {np.mean(sweet_A_warpages):.1f} nm")
    print(f"  CV: {sweet_cv:.1f}%")
    
    print(f"\nChaos Cliff (k_azi 0.7-1.15):")
    print(f"  Mean warpage: {np.mean(cliff_warpages):.1f} nm")
    print(f"  CV: {cliff_cv:.1f}%")
    
    # Check 4: Peak warpage location
    peak_idx = np.argmax(warpage)
    print(f"\nPeak warpage: {warpage[peak_idx]:.1f} nm at k_azi={k_azi[peak_idx]:.2f}")
    
    # Assertions
    checks = []
    
    # Overall trend should be rising
    checks.append(("Rising trend", slope > 0))
    
    # Chaos cliff CV should be higher than sweet spot
    checks.append(("Chaos cliff has higher variance", cliff_cv > sweet_cv))
    
    # Baseline should be lower than peak
    checks.append(("Baseline < peak", baseline[0] < warpage[peak_idx]))
    
    print(f"\n{'='*60}")
    print("VERIFICATION CHECKS:")
    all_pass = True
    for name, result in checks:
        status = "PASS" if result else "FAIL"
        if not result:
            all_pass = False
        print(f"  [{status}] {name}")
    
    if all_pass:
        print(f"\nRESULT: ALL CHECKS PASS")
        print(f"  The k_azi chaos cliff is real and verified by {len(cases)} FEA cases.")
        print(f"  Competitors operating at k_azi 0.7-1.15 will see {cliff_cv:.0f}% variance.")
    else:
        print(f"\nRESULT: SOME CHECKS FAILED")
        sys.exit(1)
    
    print(f"{'='*60}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
