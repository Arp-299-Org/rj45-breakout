# Independent Verification Reproduction Report

VERDICT: PASS

Independent verification reviewer reproduced all design, rule, connectivity, clearance, mask, and BOM identity checks directly from the saved project source files (`board/rj45_breakout.kicad_sch`, `board/rj45_breakout.kicad_pcb`, `board/rj45_breakout.kicad_dru`, `board/rj45_breakout.kicad_pro`, `board/rj45_breakout.pretty/*.kicad_mod`, `board/exports/rj45_breakout-bom.csv`, `hardware/reference/parts.json`, `board/DECISIONS.md`, `board/SPACE.md`).

## 1. Source SHA-256 Digests
- `board/rj45_breakout.kicad_sch`: `382ad3643b8def54011743686315e7b443f7e680b439d52c7bab0d5f6d4ac718`
- `board/rj45_breakout.kicad_pcb`: `67f2c14f021f772807f157ba457641d184f63f9d35f16024a6f6077f364c80b3`

## 2. Fresh KiCad CLI ERC & DRC Reproduction (KiCad 10.0.8)
- **ERC (`kicad-cli sch erc --severity-all --exit-code-violations`):** Exit `0`; `0` errors, `0` warnings, `0` exclusions.
- **DRC with schematic parity & refill (`kicad-cli pcb drc --schematic-parity --refill-zones --severity-all --exit-code-violations`):** Exit `0`; `0` violations, `0` schematic parity errors, `0` unconnected items, `0` `lib_footprint_mismatch`.
- **`board/reports/documented-drc-exclusions.json`:** `"accepted_warning_refs": []` (empty).

## 3. Independent Geometry & Electrical Reproduction
- **Board outline (`Edge.Cuts`):** Closed loop of `4` lines + `4` corner arcs (`36.000 x 35.000 mm`, `1.5000 mm` corner fillet radius).
- **Footprints & library parity:** `J1` at `(18.0, 6.475)` `180 deg`, `J2` at `(18.0, 25.0)` `0 deg`, `H1..H4` at corners `(3.5, 3.5)`, `(32.5, 3.5)`, `(3.5, 31.5)`, `(32.5, 31.5)`. Every pad set matches its `.kicad_mod` copy (`True`).
- **Copper routing (`/RJ45_1`..`/RJ45_8`):** `24` `F.Cu` segments (`3` per net), `0` vias, `0` `B.Cu` copper, `0.25 mm` width on every segment (`>= R1 0.25 mm`). Unbroken endpoint chains from `J1.N` to `J2.N` with vertical (`90.0 deg`) centered exits and `135.0 deg` obtuse corners:
  - `/RJ45_1`: `J1(14.430,13.250)->J2(9.110,26.600)`, `15.554 mm`
  - `/RJ45_2`: `J1(15.450,13.250)->J2(11.650,23.400)`, `11.724 mm`
  - `/RJ45_3`: `J1(16.470,13.250)->J2(14.190,26.600)`, `14.294 mm`
  - `/RJ45_4`: `J1(17.490,13.250)->J2(16.730,23.400)`, `10.465 mm`
  - `/RJ45_5`: `J1(18.510,13.250)->J2(19.270,26.600)`, `13.665 mm`
  - `/RJ45_6`: `J1(19.530,13.250)->J2(21.810,23.400)`, `11.094 mm`
  - `/RJ45_7`: `J1(20.550,13.250)->J2(24.350,26.600)`, `14.924 mm`
  - `/RJ45_8`: `J1(21.570,13.250)->J2(26.890,23.400)`, `12.354 mm`
- **Minimum clearances:** segment-to-segment `0.4712 mm` (`>= 0.20 mm`), segment-to-pad `0.5450 mm` (`>= 0.20 mm`), pad-to-pad `0.3200 mm` (`>= 0.20 mm`), copper-to-edge `3.0500 mm` (`>= 0.30 mm`), copper-to-NPTH `1.4828 mm` (`>= 0.30 mm`).
- **Pad masks & hand-solder joints:** All `J1` (`8` signal + `2` anchor) and `J2` (`8` signal) SMD pads carry `F.Cu`, `F.Mask`, `F.Paste`; `0` hand-soldered joints.

## 4. BOM & LCSC Identity Consistency
- Schematic, PCB footprint properties, `board/exports/rj45_breakout-bom.csv`, and `hardware/reference/parts.json` match identically for `J1` (`Heling` `MJ56881-B011-HLRN1-C`, `LCSC` `C501473`) and `J2` (`hanxia` `HX PZ2.54-1x8P TP-ZQ`, `LCSC` `C42453975`). `H1..H4` carry `in_bom=no` and `exclude_from_bom exclude_from_pos_files` and are excluded from the BOM CSV.
