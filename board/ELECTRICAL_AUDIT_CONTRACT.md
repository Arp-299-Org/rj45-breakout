# Electrical audit

The rules this board's electrical audit computes from the saved board, each
with its basis. The Constraints card keeps this file current; the Routing
batch, Board checks and Verification cards check the board against it. The
script is the one the board description names under `electrical_audit`; until
the board has one, that key is null and the checks say the audit was skipped.
A skipped audit proves nothing about these rules.

## Intent

Passive 1-to-1 breakout of 8 RJ45 (8P8C) contacts (`RJ45_1` through `RJ45_8`) from the right-angle jack (`J1`) to the 1x8 2.54 mm vertical male header (`J2`) for workbench probing, patching, and breadboarding, preserving T568B pair adjacency and full contact current capacity (`1.5 A`).

## Facts the rules rest on

- **Layer stack:** 2-layer `1.6 mm` FR-4, 1 oz (`35 um`) outer copper (`F.Cu`, `B.Cu`), JLCPCB standard 2-layer process (min trace/space `0.127 mm`, min copper-to-edge `0.30 mm`, min drill `0.30 mm`, plated hole tolerance `+0.13 / -0.08 mm`).
- **Passive topology:** Pure point-to-point passive breakout with no active silicon, no firmware, no decoupling capacitors, and no dedicated power or ground planes required (no shield pin per `board/DECISIONS.md`, 2026-11-25).
- **Connector ratings:**
  - `J1` (Heling `MJ56881-B011-HLRN1-C`, LCSC `C501473`, datasheet p. 1): rated `1.5 A`, `40 mOhm` max contact resistance, `500 VAC` dielectric withstand, `0.70 mm` signal pad width on `1.02 mm` pitch (`0.32 mm` inter-pad gap).
  - `J2` (hanxia `HX PZ2.54-1x8P TP-ZQ`, LCSC `C42453975`, datasheet p. 1): rated `3.0 A`, `20 mOhm` max contact resistance, `1000 VAC` dielectric withstand, `1.02 mm` pad width on `2.54 mm` staggered pitch.
- **Return paths and bus timing:** Passive DC/low-speed/patch breakout; signals are user-supplied across the 8 independent conductors (`RJ45_1`..`RJ45_8`). Keeping `J1` facing the north edge (`180 deg`) and `J2` along the south edge (`0 deg`) aligns pins `1`..`8` in monotonic west-to-east order so T568B pairs (`1/2`, `3/6`, `4/5`, `7/8`) run straight and uncrossed on `F.Cu` with short, matched lengths (<`25 mm`).

## Net classes

- **`Default`:** Contains all 8 signal nets (`RJ45_1` through `RJ45_8`). Trace width `0.25 mm`, clearance `0.20 mm` (local choice: `0.25 mm` at 1 oz Cu external carries >`1.5 A` with minimal rise over `<25 mm` run length and clears `J1`'s `0.32 mm` inter-pad gap cleanly).
- **Unassigned pads/holes:** `J1` mechanical SMT anchor tabs and `H1`..`H4` M3 NPTH mounting holes carry no electrical net. No routed net sits outside `Default`.

## Rules (each is a script check; a number in the report, not an opinion)

| # | Rule | Gate | Basis |
|---|---|---|---|
| R1 | Minimum trace width on `RJ45_1`..`RJ45_8` | `>= 0.25 mm` | Local choice (2026-11-25); exceeds JLCPCB `0.127 mm` min and carries `J1` `1.5 A` rating |
| R2 | Minimum copper-to-copper clearance | `>= 0.20 mm` | Local choice (2026-11-25); exceeds JLCPCB `0.127 mm` min and preserves solder-mask dams |
| R3 | Copper-to-edge and copper-to-NPTH clearance | `>= 0.30 mm` | JLCPCB 2-layer capability (`0.30 mm` edge/NPTH margin) |
| R4 | Planar routing on `F.Cu` with zero vias and zero crossings | `0` vias, `0` `B.Cu` signal segments | Local choice (2026-11-25); monotonic pin `1..8` alignment (`J1` `180 deg`, `J2` `0 deg`) |
| R5 | Centered 45-degree pad exits, no acute angles or acid traps | `0` route-quality errors | Route quality and track-craft contract (`kicad_route_quality.py`) |

## First routing batch

- **Nets:** `RJ45_1`, `RJ45_2`, `RJ45_3`, `RJ45_4`, `RJ45_5`, `RJ45_6`, `RJ45_7`, `RJ45_8` (all 8 signal nets in one fanout batch).
- **Routing mode:** `Mode: ipc` (unobstructed single-layer `F.Cu` fanout channel between `J1` and `J2`, suited to checked atomic IPC chunks via `scripts/kicad_lay.py`).
- **Stop:** All 8 nets routed with `0` DRC violations, `0` unconnected items, `0` route-quality errors/warnings, and centered pad exits confirmed on saved board.

## What the checks measure

Say, for each rule, what the script's model leaves out. These hold for the
tool's scripts as they are and for most audits like them:

- A track-to-track spacing does not cover pads, vias or dense fanout; those
  still need inspection against the copper-clearance rules.
- Curved tracks measured by their endpoint chord are not arc checks: inspect
  arcs separately.
- A sampled return path is an estimate: a clear result does not establish fill
  on both sides or model return current.
- A path length the model cannot establish (arcs, custom pads, contact through
  a zone) is a finding, not proof that the net is disconnected.
- A loop area or similar figure is a reproducible geometric estimate, not an
  electromagnetic simulation or a noise limit.

## Where subsystems meet

When a rule can be met only by breaking another, that is not the audit's call.
It is written up as a decision for the owner with both costs. The order the
owner weighs them in is recorded in `board/DECISIONS.md`; list it here with
the reason for each place.

## Method

Keep the audit script matched to the circuit, the datasheets, the firmware
interface settings and the rule table above; a changed part, pin or setting
reopens the Constraints card.
