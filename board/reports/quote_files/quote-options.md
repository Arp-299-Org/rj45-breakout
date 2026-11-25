# Quote Options: RJ45_BREAKOUT (Rev A)

- **Branch / Base Commit:** `feat/rj45-breakout-design` at `72f2727`
- **Board file:** `board/rj45_breakout.kicad_pcb` (`sha256: 67f2c14f021f772807f157ba457641d184f63f9d35f16024a6f6077f364c80b3`)
- **Schematic file:** `board/rj45_breakout.kicad_sch` (`sha256: 382ad3643b8def54011743686315e7b443f7e680b439d52c7bab0d5f6d4ac718`)
- **Prepared provisional files (`board/reports/quote_files/fab/`):**
  - Gerber + Drill + Job archive: `board/reports/quote_files/fab/RJ45_BREAKOUT.zip` (`sha256: 4331038fca3bc901fbcbcf02ff73bc75a4c306e4d3ca07ee922d2f3501e664b9`)
  - IPC-D-356 netlist: `board/reports/quote_files/fab/netlist.ipc`
  - JLCPCB SMT BOM: `board/reports/quote_files/fab/RJ45_BREAKOUT_SMT_bom.csv` (`2` factory parts: `J1` `C501473`, `J2` `C42453975`)
  - JLCPCB SMT CPL: `board/reports/quote_files/fab/RJ45_BREAKOUT_SMT_positions.csv` (`top` side only; `J1` `180.0 deg`, `J2` `0.0 deg`)
  - Hand assembly sheet: `board/reports/quote_files/fab/HAND_SOLDER.md` (`0` manual parts)
  - Assembly manifest: `board/reports/quote_files/fab/assembly-manifest.json` (`18` top paste flashes, `0` bottom, BOM/CPL sets match)

## Verified Component Pricing & Stock (`board/reports/stock/listings.json`, read 2026-11-25T19:46:00Z)

| Ref | MPN | LCSC ID | Class | Stock | Verified Unit Price |
|---|---|---|---|---|---|
| `J1` | `MJ56881-B011-HLRN1-C` | `C501473` | Extended | `3,248` | `$0.5807` |
| `J2` | `HX PZ2.54-1x8P TP-ZQ` | `C42453975` | Extended | `1,740` | `$0.0959` |
| **Total BOM components / board** | | | **2 Extended** | | **`$0.6766`** |

## Comparable Supplier Options (Same Board Revision)

| Option | Assembly Scope & Qty | Component BOM (Verified) | Fab / PCBA / Shipping (Quote Needed) | Tradeoffs |
|---|---|---|---|---|
| **Option A1 (Recommended)** | **JLCPCB 2-layer `1.6 mm` FR-4 + Economic PCBA (Front SMT, Qty 5)** (`2` SMT parts per board, `0` hand soldering) | `$3.3830` total (`5 x $0.6766`) plus JLCPCB attrition/reel minimums if any | Upload `RJ45_BREAKOUT.zip`, `RJ45_BREAKOUT_SMT_bom.csv`, and `RJ45_BREAKOUT_SMT_positions.csv` to JLCPCB cart for exact PCB fab, Economic PCBA setup, stencil, `2 x` Extended feeder loading fees, and shipping/tax | Zero bench soldering; both `J1` (`1.02 mm` fine-pitch leads + locating pegs) and `J2` arrive factory-assembled and ready to plug into a breadboard or RJ45 patch cable; higher fixed setup/feeder overhead amortized over only 5 boards |
| **Option A2** | **JLCPCB 2-layer `1.6 mm` FR-4 + Economic PCBA (Front SMT, Qty 10)** (`2` SMT parts per board, `0` hand soldering) | `$6.7660` total (`10 x $0.6766`) | Same upload set at Qty 10 for cart quote | Fixed PCBA setup, stencil, and two Extended feeder fees amortize across 10 assembled boards instead of 5, lowering per-board delivered cost substantially if you want spares or extras for giveaway |
| **Option B** | **JLCPCB 2-layer `1.6 mm` FR-4 Bare PCB Only (Qty 5 or 10) + DIY Hand Assembly** | Source `MJ56881-B011-HLRN1-C` (`C501473`) and `HX PZ2.54-1x8P TP-ZQ` (`C42453975`) independently | Upload `RJ45_BREAKOUT.zip` only for bare PCB quote | Eliminates PCBA setup and Extended feeder charges, but requires hot-air/reflow or careful drag-soldering on `J1`'s `0.70 mm` width / `1.02 mm` pitch pins, large `2.94 x 5.00 mm` metal anchor tabs, and staggered `J2` SMD pads |

## Next Action (`Quote` Card, Owner Gate)
Upload the provisional files under `board/reports/quote_files/fab/` to JLCPCB to capture itemized PCB fab, components, stencil/setup, Extended feeder loading, assembly, and shipping quotes at your chosen quantity (`5` vs `10`) and confirm `Quote` before sealing the production archive at `Package`.
