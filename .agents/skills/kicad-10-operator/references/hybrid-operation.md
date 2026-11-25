# Hybrid KiCad operation

## The routes

Use these methods only when they are within the owner's chosen workflow.
Choose a method for the task and pair it with checks for what it misses.
Only one routing wrapper was timed; do not assume every shortcut is faster.

| Route | Best use | Misses, and what covers it |
|---|---|---|
| Saved files read as s-expressions | Read saved-state questions when useful | Unsaved edits: inspect the editor, or use IPC `get_as_string` if allowed. How it looks: the editor |
| Guarded schematic edit | Repeated or exact changes in the schematic | Whether the sheet still reads well: look. Electrical intent: netlist, ERC and the project's required review |
| IPC | Exact moves and bulk changes in the PCB, unsaved-state queries, refill, save | Obstacle negotiation: the interactive router. Rules: CLI DRC. Judgment: look |
| Offline pcbnew script on a copy | A batch the owner chose to run as a re-runnable transform | The open editor: reload only when authorized and safe |
| Isolated KiCad CLI | ERC, DRC, netlists, plots, renders, repeatable exports | GUI state, readability, placement quality, return paths: look |
| Native KiCad GUI | Interactive routing, symbol moves that keep wires, placing by eye, F8, visual review | Exact preservation: compare the saved file |

Use complementary tools; do not count the same underlying check multiple times.

## What IPC can and cannot do

`kicad-python` 0.7.1 on KiCad 10.0.7. "Run" was run on the Mac on a
disposable copy with the saved file compared; "source" is only read in the
library.

| Job | IPC | Evidence | Pair with |
|---|---|---|---|
| Read anything, unsaved included | `get_footprints`, `get_active_layer`, `get_visible_layers`; also `get_tracks`, `get_vias`, `get_pads`, `get_zones`, `get_text`, `get_nets`, `get_items_by_net`, `get_connected_items`, `get_as_string` | Run, source | |
| Move | `position`, `update_items`; for a block, the same offset on every part | Run (M) (W): clean, one `(units` block dropped | |
| Move a via or footprint with its tracks | The item and every attached track end, in one commit | Run: a via moved alone left its tracks behind. 10.0.8, a via: its three track ends moved with it, one Cmd+Z restored all four, the saved file changed only those coordinates (M) | CLI DRC: no collision check during the update |
| Rotate | `orientation`, `update_items` | Run: **dropped the 3D model line** (64 to 63), the `(units` block, and rewrote silk and fab items with new ids; stored geometry shifted about a micron and KiCad reported a library-footprint mismatch | `R` or `E` in the GUI; or count `(model` and restore, and Tools > Update Footprints from Library |
| Lock | `locked` | Source | Status bar |
| Add, change, delete tracks and vias | `create_items`, `update_items` (widths, nets), `remove_items` (by id) | Run. 10.0.8, a delete: one Cmd+Z restored it, the saved file lost only that segment (M) | CLI DRC: nothing checks rules on the way in. Check each via's attachment on the intended copper layers as well as loose track ends: an endpoint graph without via nodes misses an unfinished via |
| Move a reference field, or a board text | `update_items` (the footprint, for its field) | Run: 3D model lines kept. 10.0.8: the saved file changed only the field's or text's `(at` line; every `(model` and `(units` line kept (M) | Look |
| Reshape a rule area | The outline, `update_items` | Run | Look |
| Add zones and text | `create_items` | Source | CLI DRC |
| One undo step | `begin_commit`, `push_commit`, `drop_commit` | Run: `drop_commit` restores. 10.0.8: one Cmd+Z undoes one pushed commit, whatever it held (M) | |
| Refill, save | `refill_zones`, `save`; a refill needs `KiCad(timeout_ms=180_000)`, the default is 2 s | Run | Inspect in the editor |
| Reload | `revert` | Run: 10.0.8, the file put back from a copy under an editor holding a saved later version; afterwards every track, arc and via id and every item read back from the editor matched the file (M). Source: it discards unsaved edits without asking | Check that no work to keep will be discarded |
| Select | `add_to_selection`, including a rule area as Repeat Layout's source | Run | Inspect in the editor |
| Steer the view | `set_active_layer`, `set_visible_layers` | Source | Inspect in the editor |
| Flip | No. `layer` set B.Cu and left the pads on F.Cu | Run: a broken part | `F` in the GUI |
| Route around obstacles | No router call | Source | `X` in the GUI |
| Run DRC or ERC | No | Source | CLI |
| Update from the schematic | No | Source | `F8` |
| Schematic | The library marks `Schematic` "KiCad 11", and `KiCad` offers only `get_board` | Source | Guarded edit, GUI |

"KiCad is busy" (`AS_BUSY`), or no answer while the chooser is open, means a
dialog or an armed tool in the editor, not a hung API: diagnose with
`scripts/kicad_ipc_status.py`. Not every dialog blocks: on 10.0.8 an IPC
delete went through with File > Page Settings open (M). `run_action` is documented as unstable: leave it.

## Guarded schematic edits

A guarded saved-file edit is a hybrid method, not an editor gesture. Use it
only when the actual project and owner permit it; check the source identity,
the resulting diff, connectivity and ERC, then inspect the reloaded design.

## Offline script on a copy

An offline board script operates on a saved copy and does not update an open
editor. The owner's scope and the project's procedure decide whether it
may be used and how the result is installed and reviewed.

What pcbnew accepted on the Mac, each in its own process:

| Job | Works | Does not |
|---|---|---|
| Net list | `board.GetNetInfo()` | `GetNetinfo` is absent |
| Add a net | `board.Add(pcbnew.NETINFO_ITEM(board, name, code))` | `AppendNet` is absent |
| Set a footprint field | `fp.SetField(name, value)` | `pcbnew.PCB_FIELD(fp)` raises |
| Zone clearance | `zone.SetLocalClearance(nm)` | `SetZoneClearance` is absent |
| Fill zones | `pcbnew.ZONE_FILLER(board).Fill(board.Zones())` on a board from `LoadBoard`, its `.kicad_pro` beside it | |
| Via width | `via.SetWidth(nm)` | |
| Layers | `board.GetLayerID(name)`: F.Cu 0, B.Cu 2, In1.Cu 4, In2.Cu 6, not in stack order | |
| A footprint copied on the board with new UUIDs | `fp.Duplicate(False)` (fall back to `Duplicate()` on a TypeError), `.Cast()`, `SetReference`, `SetPosition`, `board.Add`: 11 new UUIDs on a mounting hole (M) | |
| A footprint's library id | `fp.SetFPID(pcbnew.LIB_ID(nickname, name))` | `fpid.SetLibItemName(str)`: wants a `UTF8` |
| Tracks once a footprint was added | Read `board.GetTracks()` and keep the list before `board.Add(footprint)` (M) | `board.GetTracks()` afterwards: `'SwigPyObject' object is not iterable` (10.0.8) |
| A cut in a rule area | `zone.Outline().AddHole(chain, 0)` with a closed `SHAPE_LINE_CHAIN`, then `zone.HatchBorder()` (M) | |

On Windows, `fp.Flip` before `board.Add`, and a fill on a board made with
`pcbnew.BOARD()`, each killed the process; the Mac survived both. Add first,
and fill a loaded board.

## Canonical files

- `.kicad_sch`: schematic connectivity, symbols, references, values, and
  assigned footprints.
- `.kicad_pro`: project settings, constraints, net classes, and layer setup.
- `.kicad_mod`: footprint pads, fabrication, silkscreen, courtyard, and package
  metadata.
- `.kicad_pcb`: board outline, placement, copper, vias, zones, and board
  graphics after update from the schematic.
- Reports, renders, netlists, and plots: derived evidence, not source authority.

If generated source and GUI edits overlap, explicitly propagate the edit back
to the generator, transfer ownership of that region to KiCad, or retire the
generator for that artifact. Never leave a correct GUI result that a later
regeneration will silently erase.

Before IPC evidence, require exactly one intended project-owned editor for
the target. Duplicate same-title or stand-alone editors make semantic state
ambiguous.

## Geometry checks

Reuse stored integer-nanometer endpoints when joining IPC tracks and vias.
In kicad-python 0.7.1, `from_mm` uses `int(value_mm * 1_000_000)`: a nominal
134.2 mm became 134199999 nm (M). Read the actual coordinates for joins and
round newly calculated points to integer nanometers.

Model oval holes as stadiums in offline geometry checks; a circle of the
larger diameter reports false failures.
