#!/usr/bin/env python3
"""
MULTI-DIE SCALING VERIFICATION
===============================
Proves that warpage problem scales catastrophically with HBM die count.

This script loads multi_die_comparison.json and verifies:
1. 3 HBM configuration: 0% pass rate (64 FEM cases)
2. 5 HBM configuration: 0% pass rate (64 FEM cases)
3. 8 HBM configuration: 0% pass rate (64 FEM cases)
4. Warpage increases with die count (monotonic scaling)

Total: 192 verified FEM cases from Cloud HPC.
ALL configurations show 0% pass rate without our optimization.

Usage:
    python3 verify_multi_die_scaling.py

Evidence file: EVIDENCE/multi_die_comparison.json
"""

import json
import os
import sys

# ─────────────────────────────────────────────────────────────────────────────
# Load the multi-die comparison data
# ─────────────────────────────────────────────────────────────────────────────

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
EVIDENCE_DIR = os.path.join(os.path.dirname(SCRIPT_DIR), "EVIDENCE")
DATA_FILE = os.path.join(EVIDENCE_DIR, "multi_die_comparison.json")

print("=" * 70)
print("MULTI-DIE SCALING VERIFICATION")
print("=" * 70)

# Load the data
with open(DATA_FILE) as f:
    data = json.load(f)

print(f"\nLoaded {DATA_FILE}")
print(f"Configurations tested: {len(data)}")

# ─────────────────────────────────────────────────────────────────────────────
# Verify each configuration
# ─────────────────────────────────────────────────────────────────────────────

total_cases = 0
total_passes = 0
all_pass_rates = []

print("\n" + "-" * 70)
print(f"{'Configuration':<25} {'Samples':>8} {'Pass':>6} {'Fail':>6} {'Pass%':>8} {'Min (µm)':>10} {'Max (µm)':>10}")
print("-" * 70)

for config in data:
    name = config['config']
    n_hbm = config['n_hbm']
    samples = config['samples']
    passes = config['passes']
    fails = config['fails']
    pass_rate = config['pass_rate_pct']
    w_min = config['warpage_min']
    w_max = config['warpage_max']
    
    total_cases += samples
    total_passes += passes
    all_pass_rates.append(pass_rate)
    
    print(f"{name:<25} {samples:>8} {passes:>6} {fails:>6} {pass_rate:>7.1f}% {w_min:>10.1f} {w_max:>10.1f}")

print("-" * 70)
print(f"{'TOTAL':<25} {total_cases:>8} {total_passes:>6} {total_cases - total_passes:>6}")

# ─────────────────────────────────────────────────────────────────────────────
# Verification assertions
# ─────────────────────────────────────────────────────────────────────────────

print("\n" + "=" * 70)
print("VERIFICATION ASSERTIONS")
print("=" * 70)

checks = []

# 1. All pass rates should be 0%
all_zero = all(r == 0.0 for r in all_pass_rates)
checks.append(("All configurations show 0% pass rate", all_zero))

# 2. Total should be 192 cases (3 configs × 64 samples)
checks.append((f"Total cases = {total_cases} (expected 192)", total_cases == 192))

# 3. Warpage increases with HBM count (monotonic scaling)
min_warpages = [c['warpage_min'] for c in sorted(data, key=lambda x: x['n_hbm'])]
monotonic = all(min_warpages[i] <= min_warpages[i+1] for i in range(len(min_warpages)-1))
checks.append(("Minimum warpage increases with HBM count", monotonic))

# 4. Max warpage at 8 HBM exceeds 25,000 µm (catastrophic)
max_8hbm = [c for c in data if c['n_hbm'] == 8][0]['warpage_max']
checks.append((f"8 HBM max warpage = {max_8hbm:.0f} µm (catastrophic >25,000)", max_8hbm > 25000))

# 5. Even 3 HBM minimum exceeds 1,000 µm (far above 20µm spec)
min_3hbm = [c for c in data if c['n_hbm'] == 3][0]['warpage_min']
checks.append((f"3 HBM minimum warpage = {min_3hbm:.0f} µm (>>20 µm spec)", min_3hbm > 1000))

# Report
all_pass = True
for desc, result in checks:
    status = "PASS" if result else "FAIL"
    if not result:
        all_pass = False
    print(f"  [{status}] {desc}")

# ─────────────────────────────────────────────────────────────────────────────
# Conclusion
# ─────────────────────────────────────────────────────────────────────────────

print("\n" + "=" * 70)
if all_pass:
    print("ALL VERIFICATIONS PASSED")
    print()
    print("CONCLUSION: The warpage problem scales CATASTROPHICALLY with HBM count.")
    print(f"  - 3 HBM: {min_3hbm:.0f} - {data[0]['warpage_max']:.0f} µm (0% pass)")
    print(f"  - 5 HBM: {data[1]['warpage_min']:.0f} - {data[1]['warpage_max']:.0f} µm (0% pass)")
    print(f"  - 8 HBM: {data[2]['warpage_min']:.0f} - {data[2]['warpage_max']:.0f} µm (0% pass)")
    print()
    print("WITHOUT spatially-varying density optimization, multi-die packaging")
    print("is IMPOSSIBLE at current and future HBM stack counts.")
    print("This proves the technology becomes MORE valuable as die counts increase.")
else:
    print("SOME VERIFICATIONS FAILED — investigate data integrity")
    sys.exit(1)

print("=" * 70)
