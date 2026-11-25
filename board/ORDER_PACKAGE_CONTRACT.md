# Order package

How the order package is made from the board, and what it must pass before it
is orderable. No purchase is authorized by this page. The tool's package
scripts write files for JLCPCB fabrication and assembly; another assembler
needs its own scripts.

## Intent

An order that produces a first article made from the current approved board:
the copper the editor shows, the parts the schematic names, every polarized
part facing the way the board says. The package must be impossible to confuse
with an older export.

## What the package contains

| File | Produced by | Consumed by |
|---|---|---|
| `<NAME>_<date>.zip`, Gerbers and Excellon drills, absolute origin | `scripts/kicad_generate_fabrication_archive.py` | fabrication upload |
| `netlist.ipc`, the IPC-D-356 test netlist | `scripts/kicad_generate_fabrication_archive.py` | `scripts/kicad_package_production.py`, which re-exports it from the board and compares the two line by line |
| `<NAME>_<date>_SMT_bom.csv`, `_SMT_positions.csv` | `scripts/kicad_generate_jlc_source_files.py` then `scripts/kicad_finalize_jlc_outputs.py` | assembly upload |
| `<NAME>_<date>_bom.csv`, `_positions.csv`, `_designators.csv` (all parts) | same | `scripts/kicad_finalize_jlc_outputs.py`, which checks them against the board and writes the SMT files from them; they name the hand-soldered parts too, so they are never uploaded |
| HAND_SOLDER.md | `scripts/kicad_finalize_jlc_outputs.py`, from the board and the description's hand_solder_notes | the builder at the bench |
| assembly-manifest.json | `scripts/kicad_finalize_jlc_outputs.py` | the record of what was ordered |
| package-manifest.json, .sha256 | `scripts/kicad_package_production.py` | the record of what was ordered |

`<NAME>` matches the description's `package_name`. All of it is generated into
the description's `production` folder from the exact saved board, whose hash
is recorded. The factory list, the hand-solder list and the polarized-part
list come from the board at packaging time, not from this page. A supplier
part number alone does not assign a part to factory assembly: the SMT files
hold exactly the fitted parts the board marks SMD that carry a part number;
every other fitted part is hand-soldered and listed in HAND_SOLDER.md, and DNP
parts are in no order file. Off-board items need a separate procurement entry.

Package readiness also requires current stock, quantity, price and assembly
eligibility for the chosen supplier, plus the owner's confirmed quantity and
quote. Before the owner chooses an assembly scope, compare the baseline with
an itemized fuller assembly option on the same board revision and quantity.
Do not assume the assembler can install every manual part, and do not treat
this comparison as approval to change the production BOM or CPL.

## Gates ("orderable" means all of these, fresh against the packaged board)

| # | Gate | Number |
|---|---|---|
| G1 | ERC on the schematic, errors and warnings included | 0 |
| G2 | DRC with schematic parity, errors and warnings | 0 copper, 0 unconnected, 0 parity, 0 `lib_footprint_mismatch`: the reference list in the description's `drc_exclusions` file is empty and bound to this revision |
| G3 | Route quality | 0 errors; 0 unreviewed warnings (any remaining warning must match a verified `FINE AS IS` verdict in an adopted routing receipt) |
| G4 | The board's electrical audit against `board/ELECTRICAL_AUDIT_CONTRACT.md` | pass; the waiver file's hash recorded in the package manifest; no waiver added while packaging. "None for this board" when the description names no audit |
| G5 | Pad mask report | 0 pads without an aperture |
| G6 | The board's full board audit | pass; "none for this board" when the description names none |
| G7 | BOM/CPL: every factory part has a supplier part number; BOM and CPL name the same set; every coordinate and side matches the board; every angle matches under the assembler's reading (for JLCPCB: front, KiCad's angle; back, 180 minus KiCad's angle). Complete paste geometry, including polygon regions, matches a fresh export | all true, checked by `kicad_finalize_jlc_outputs.py` and the packager; a correct CPL does not replace G11 |
| G8 | Fabrication archive: every copper layer the board has, in stack order (front, any inner layers, back), front and back mask, silk and paste, Edge.Cuts, plated and non-plated drills. The tool's scripts read the copper layers from the saved board | all present, listed in the manifest |
| G9 | Freshness: every report in G1 to G6 stamped against the SHA-256 of the packaged board; the netlist derives from that board | `kicad_report_freshness.py check`: all fresh |
| G10 | Independent review of the package: reproduces G1 to G9 from the files in the package, not from the reports | pass |
| G11 | The owner's eyes: the assembler's placement preview for every polarized or orientation-sensitive part, written in `board/DECISIONS.md` with the date | written by the owner |
| G12 | No stale export: the production folder holds only this package | true |

Any special factory process (paste deposition, fixtures, plated-slot
soldering) must be confirmed on the quote before payment; correct upload
files do not prove an order includes it. Parts the owner has explicitly
deferred until after the order (an enclosure, a fixture, a dry fit) are not
gates; they stay cards after delivery.

## Making the package

Copper changes invalidate the package. Run `scripts/validate_board.py --out
<reports>/package` on the KiCad machine: it writes the gate reports under their
own names (`erc.json`; `drc.json`, which carries the schematic parity and the
unconnected items; `route-quality.json`; `electrical-audit.json`;
`pad-mask.json`; the full board audit's report), and the packager reads exactly
those from `--reports`. Stamp them there (`scripts/kicad_report_freshness.py
stamp`). The G2 reference list stays in the description's `drc_exclusions`
file with its own stamp; the packager reads it from `--exclusions`. Write the
visual inspection record in the same folder as `VISUAL_INSPECTION` (Markdown),
run step 4 with `--check-only`, run G10 on those outputs and save the critic's
report there as `G10_BOARD_CRITIC_REPORT` (Markdown) with PASS as its first
line, then run step 4 for real. The packager refuses reports that do not
describe the board being packaged. Then, in order, each through
`scripts/kicad_run.ps1 -Mode Offline -Project board`, with `$Board` the
description's `pcb` and `<NAME>` the package's base name:

1. `scripts/kicad_generate_fabrication_archive.py --board $Board --production <production> --base-name <NAME>`
2. `scripts/kicad_generate_jlc_source_files.py` (same arguments)
3. `scripts/kicad_finalize_jlc_outputs.py --production <production> --base-name <NAME> --board $Board`
4. `scripts/kicad_package_production.py --production <production> --reports <reports> --base-name <NAME> --output <folder>/<NAME>-complete-package.zip --checksum-output <folder>/<NAME>-complete-package.sha256`

How strong each staleness check is:

| Check | Basis | Survives a git checkout |
|---|---|---|
| Gate and validation reports | SHA-256 of board and schematic, in the reports' `provenance.json` | yes |
| `netlist.ipc` | re-exported at packaging time and compared line by line | yes |
| Revision names in bundle prose | text scan for another revision's `<NAME>_<date>` | yes |
| Gerber/drill archive and paste geometry | regenerated from the board and compared by the current packager | yes |
| Remaining bundle files | mtime against the board's mtime | no |

The last row is weak: a fresh clone stamps every file with the checkout time.
Only regenerating an artifact and comparing it proves derivation. No gate reads
prose for meaning; read the README you are shipping, every time.

Two traps:

- The bundle zip is not byte-reproducible (ZIP entries carry times and the
  package manifest is rewritten each run). The recorded checksum comes from
  the final packaging run; an auditor hashes the shipped file rather than
  rebuilding it.
- One checksum filename, `<NAME>-complete-package.sha256`. A second spelling
  leaves an older hash asserting that a good file is corrupt. The packager
  refuses to run while a second checksum file or another revision's
  `-complete-package.*` sits in the folder.

## Status words

connected, DRC-clean, electrically audited (only when freshly proved), packaged
(G1 to G10), orderable (G11 and G12 too), ordered (the supplier's order number
in the order evidence), delivered (receipt and incoming inspection),
hardware-accepted (the board's first-article test procedure, recorded).
