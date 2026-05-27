# Fission Compression Core v1

**Author:** David Wise  
**Date:** 2026-05-14  
**License:** CC0 1.0 Universal (Public Domain)  
**Intent:** Defensive publication — prior art disclosure under 35 U.S.C. §102

> Merit for production, not money. Level playing field.

---

## What this is

A fission-push compression engine that breathes through a zero-point.

Conventional compression pulls inward (fusion). This pushes outward, inverts at the zero-point, and returns — harvesting energy at the crossing. The system uses ternary logic (-1, 0, +1) rather than binary. Zero is an active inversion state, not absence.

---

## Core sequence (18 steps)

```
1 → 3 → 6 → 9 → 15 → 21 → 24 → 27 → 0 → 0 → 27 → 24 → 21 → 15 → 9 → 6 → 3 → 1
```

- **Steps 0–7:** expanding outward
- **Steps 8–9:** `0 → 0` — the inversion point. Energy harvested here. "God big G."
- **Steps 10–17:** contracting inward

The double-0 is not a pause. It is the active inversion event.

---

## Architecture

| Component | Value | Description |
|-----------|-------|-------------|
| Quads | 4 | Sectors rotating 90° each step |
| Fences | 0, 1, 2, 4, 8 | Progressive barriers (not binary) |
| Ternary states | -1, 0, +1 | Logic base — 0 is active |
| Plasmatonic rate | 24.5 cycles | Non-integer prevents phase lock |
| Observer recursion | 27 × 3 = 81 | Self-reference loop |
| Moat compression | value / 212 | Gate ratio |
| Saturation | 999 / 28 ≈ 35.7 loops | 999-point tracker |

---

## Quick start

**Run the Python reference implementation:**

```bash
# One 18-step cycle with full state table
python fission_core.py run

# Full cycle as JSON
python fission_core.py json

# Energy compounding: N loops toward saturation
python fission_core.py energy 10

# Fission vs fusion side-by-side
python fission_core.py compare
```

Requires Python 3.8+. No external dependencies.

**Run the visual simulation:**

Open `fission_core.html` in any browser. No server needed.

Shows: toroid breathing, sequence stepping, quad rotation, fence gates, energy bar, harvest events.

---

## Key distinctions from prior art

- **Not binary** — ternary (-1, 0, +1)
- **Not fusion** — fission pushes outward; the zero-point is traversed, not avoided
- **Not abstract math** — physical process simulation with harvest at crossing
- **Not open loop** — bounded recursive with 0/0 inversion and observer self-reference (81)

---

## Files

```
fission_core.py       Python reference implementation + CLI
fission_core.html     Visual simulation (browser, no dependencies)
CORE.md               Full build documentation — complete system description
manifest.json         Machine-readable metadata (schema.org/Dataset, JSON-LD)
LICENSE               CC0 1.0 Universal
CONTRIBUTING.md       How to build on this
```

---

## For humans

Read `CORE.md` for the complete system specification, historical lineage, and protection intent.

## For robots

Parse `manifest.json` for `coreSequence`, `fences`, `license`. Valid implementations must maintain the 0→0 inversion at steps 8–9 of the sequence.

---

## If you build on this

Credit the 18-step cycle to David Wise. That's the merit.

---

*Built with Meta AI, May 2026. Reverse-engineered from the 27-walk.*  
*CC0 1.0 Universal — no rights reserved. This is defensive publication.*
