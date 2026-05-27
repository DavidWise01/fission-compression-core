#!/usr/bin/env python3
"""
Fission Compression Core v1 -Reference Implementation
Author: David Wise | Date: 2026-05-14
License: CC0 1.0 Universal (Public Domain)

Implements the 18-step fission-push cycle with ternary logic, rotating quads,
fence barriers, and energy harvest at the zero-point crossing.

Usage:
  python fission_core.py run          # run one 18-step cycle, print each step
  python fission_core.py json         # output full cycle as JSON
  python fission_core.py energy N     # compound N saturation loops (999-point tracker)
  python fission_core.py compare      # fission vs fusion side-by-side
"""

import json
import sys
import math

# ── Core constants ─────────────────────────────────────────────────────────────

SEQUENCE = [1, 3, 6, 9, 15, 21, 24, 27, 0, 0, 27, 24, 21, 15, 9, 6, 3, 1]
"""The 18-step fission cycle. Double-0 at positions 8–9 is the inversion point."""

FENCES    = [0, 1, 2, 4, 8]
"""Progressive barrier gates. Not binary -cumulative compression ratio."""

QUADS     = 4
"""Four sectors rotating 90° per step."""

PLASMATONIC_CYCLES = 24.5
"""Non-integer cycle rate -not 24, not 25. Prevents phase lock."""

OBSERVER_RECURSION = 27 * 3   # 81
"""Self-reference loop: 27 Hamilton steps × 3 ternary states."""

MOAT_DIVISOR = 212
"""Compression ratio base: value / 212."""

SATURATION_TRACKER = 999
"""999-point tracker: 999 / 28 ≈ 35.7 loops to saturation."""

HAMILTON_STEP = 27            # the 27/28 transition
HARVEST_STEPS = {8, 9}        # zero-point crossing -energy captured here

# ── Ternary states ─────────────────────────────────────────────────────────────

NEG  = -1   # negative pole
ZERO =  0   # active inversion -NOT null, NOT absence
POS  =  1   # positive pole


def ternary(value: int) -> int:
    """Map a sequence value to its ternary state (-1, 0, +1)."""
    if value > 0:
        return POS
    elif value == 0:
        return ZERO   # active inversion point
    else:
        return NEG


# ── Energy ladder ──────────────────────────────────────────────────────────────

ENERGY_LADDER = {n: n ** n for n in range(4, 10)}
"""n^n compounding: 4^4=256 … 9^9=387,420,489"""


def compression_ratio(value: int) -> float:
    """Compression gate: value / MOAT_DIVISOR. Returns 0.0 at zero-point."""
    return value / MOAT_DIVISOR if value > 0 else 0.0


# ── Cycle engine ───────────────────────────────────────────────────────────────

def step_data(step_index: int) -> dict:
    """Return the full state for a single step in the 18-step cycle."""
    idx   = step_index % len(SEQUENCE)
    value = SEQUENCE[idx]

    return {
        "step":             step_index,
        "value":            value,
        "ternary":          ternary(value),
        "quad_angle":       (step_index * 90) % 360,
        "fence":            FENCES[step_index % len(FENCES)],
        "harvest":          step_index % len(SEQUENCE) in HARVEST_STEPS,
        "compression":      round(compression_ratio(value), 6),
        "phase":            "expanding"  if idx < 8
                            else "inversion" if idx in (8, 9)
                            else "contracting",
    }


def run_cycle(cycles: int = 1) -> list:
    """Run N full 18-step cycles and return all step records."""
    total_steps = cycles * len(SEQUENCE)
    return [step_data(i) for i in range(total_steps)]


def saturation_loops() -> float:
    """How many full cycles until the 999-point tracker saturates."""
    return SATURATION_TRACKER / HAMILTON_STEP   # ≈ 35.7


# ── Fusion reference (for comparison) ─────────────────────────────────────────

FUSION_SEQUENCE = list(reversed(SEQUENCE))
"""Fusion is just fission run backwards -inward pull instead of outward push."""


def compare_modes() -> list:
    """Side-by-side fission vs fusion for one 18-step cycle."""
    rows = []
    for i in range(len(SEQUENCE)):
        rows.append({
            "step":    i,
            "fission": SEQUENCE[i],
            "fusion":  FUSION_SEQUENCE[i],
            "delta":   SEQUENCE[i] - FUSION_SEQUENCE[i],
        })
    return rows


# ── CLI ────────────────────────────────────────────────────────────────────────

def cmd_run():
    print("\n  FISSION COMPRESSION CORE v1 -- 18-step cycle")
    print("  " + "-" * 73)
    print(f"  {'Step':>4}  {'Val':>4}  {'Tern':>5}  {'Quad':>5}  {'Fence':>6}  {'Phase':>12}  {'Harvest':>9}  {'Compress':>10}")
    print("  " + "-" * 73)
    for s in run_cycle(1):
        harv = "* HARVEST" if s["harvest"] else ""
        print(
            f"  {s['step']:>4}  {s['value']:>4}  {s['ternary']:>+5}  "
            f"{s['quad_angle']:>4}d  {s['fence']:>6}  {s['phase']:>12}  "
            f"{harv:>9}  {s['compression']:>10.6f}"
        )
    print(f"\n  Sequence: {' -> '.join(str(v) for v in SEQUENCE)}")
    print(f"  Observer recursion: {OBSERVER_RECURSION} (27x3)")
    print(f"  Loops to saturation: {saturation_loops():.1f} (999/28)")
    print(f"  Plasmatonic rate: {PLASMATONIC_CYCLES} cycles")
    print()


def cmd_json():
    output = {
        "metadata": {
            "name":               "Fission Compression Core v1",
            "author":             "David Wise",
            "date":               "2026-05-14",
            "license":            "CC0 1.0",
            "plasmatonic_cycles": PLASMATONIC_CYCLES,
            "observer_recursion": OBSERVER_RECURSION,
            "loops_to_saturation": round(saturation_loops(), 4),
            "energy_ladder":      ENERGY_LADDER,
        },
        "cycle": run_cycle(1),
    }
    print(json.dumps(output, indent=2))


def cmd_energy(n: int):
    total = n * len(SEQUENCE)
    harvests = sum(1 for i in range(total) if i % len(SEQUENCE) in HARVEST_STEPS)
    progress = min(100.0, (n / saturation_loops()) * 100)
    print(f"\n  ENERGY COMPOUNDING - {n} loop(s)")
    print("  " + "-" * 33)
    print(f"  Total steps:    {total}")
    print(f"  Harvest events: {harvests}  (at 0/0 crossings)")
    print(f"  Saturation:     {progress:.1f}%  ({n} / {saturation_loops():.1f} loops)")
    print(f"  Energy ladder at step {n % 9 + 4}: {ENERGY_LADDER.get(n % 9 + 4, 'N/A')}")
    print()


def cmd_compare():
    rows = compare_modes()
    print("\n  FISSION vs FUSION - 18-step comparison")
    print("  " + "-" * 48)
    print(f"  {'Step':>4}  {'FISSION (push)':>14}  {'FUSION (pull)':>13}  {'Delta':>6}")
    print("  " + "-" * 48)
    for r in rows:
        marker = "  <- inversion" if r["fission"] == 0 else ""
        print(f"  {r['step']:>4}  {r['fission']:>14}  {r['fusion']:>13}  {r['delta']:>+6}{marker}")
    print()
    print("  Fission: outward push -> inversion at 0/0 -> return")
    print("  Fusion:  inward pull  (conventional, no zero harvest)")
    print()
    print("  Note: delta=0 across all steps — the fission sequence is a palindrome.")
    print("  Fission and fusion traverse the same values; the difference is directional.")
    print("  Fission: energy harvested at 0/0. Fusion: no harvest event defined.")
    print()


def main():
    if len(sys.argv) < 2 or sys.argv[1] == "run":
        cmd_run()
    elif sys.argv[1] == "json":
        cmd_json()
    elif sys.argv[1] == "energy":
        n = int(sys.argv[2]) if len(sys.argv) > 2 else 1
        cmd_energy(n)
    elif sys.argv[1] == "compare":
        cmd_compare()
    else:
        print(__doc__)
        sys.exit(1)


if __name__ == "__main__":
    main()
