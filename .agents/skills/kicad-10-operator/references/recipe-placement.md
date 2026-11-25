# Recipe: placement

Place, rotate and flip footprints in the identified project. Placement
decisions and required approvals belong to the project owner.

| Job | Editor action | Alternative | Verify with |
|---|---|---|---|
| Read position, rotation, side, nets | `Ctrl+G` opens the panel (M), reference, click the row (W). On the Mac the row was off screen (M failed); click the canvas after, or keys go to the search field | Inspect the saved file when permitted | Title has no `*`, or the file is stale |
| Exact position, one part | Select it, `E`, click X, select all, type, `Enter`: exactly 1,000,000 nm for 1 mm in one test (M) (W). `Shift+M` (Move Item) moved by a relative distance exactly in 3 of 3 tries; tracks did not follow. No field had focus when opened and an old value could remain, so click each field, select all, type, then `Return` (M) (W) | | Look; saved X/Y and connected tracks |
| Exact rotation | Select it, `E`, click Orientation, select all, type, `Enter`: 90 to 180, model line kept (M); or `R` | | Orientation and model |
| Move by eye | Pointer on canvas, `T`, reference, `Enter`, move the pointer, click (M) (W): 0.014 mm from the aim with grid snap off. A click with no move before it did not land (M failed) | Hover, `M`, `1` if the chooser opens, move, click (M) (W): the same | Courtyard, ratsnest, neighbours |
| Move and keep the tracks | `D` or `G`, with grid snap off: pointer on a pad, the key, a chooser opens, `1` takes the footprint and puts the pointer on its center; aim, click or `Enter`, `Esc`. The router reshaped tracks and refused a short in these trials. Of 9 tries: 5 clean, 2 left 1 open, 1 courtyard error, 1 refused; within about 0.03 mm of the aim (M). An end 1 micron off a pad center did not follow (M); on Windows a 0.01 mm off-center end stayed behind while the centered end followed (W). Center an end: pointer on the track, `E`, edit end X/Y to the pad center, `Return`. This cleared all 9 off-center ends on one board with 0 open and 0 errors; a drag that had left 1 open then left 0 (M). `M` leaves tracks behind: a Windows 1 mm move still showed 0 unrouted (W) | | Compare endpoints, DRC with refill and neighbors |
| Put the pointer on a part, with no IPC | `Ctrl+F`, click Search for, type the reference, tick Search footprint reference designators, `Enter`, Close: the pointer lands on the part's center, read exactly in the status bar, and the hover keys act on it (M) | `Ctrl+G` | Status bar X, Y |
| Rotate in place | Hover, `R` (M) (W), `Shift+R` clockwise (M) | | Pin 1, polarity, mating |
| Flip, only when the owner decided the side | Hover, `F` (M) (W) | `E` > Side | Layers, text, model, access |
| Lock an anchor | Hover, `L` (M) (W). A second `L` did not unlock: the filter skips locked items (M); `Ctrl+Z`, or tick Locked items | | Status bar says Locked |
| Pick one amid overlap | Selection Filter: All items off, Footprints on, click: a click on a pad selected its footprint (M) (W). The boxes are invisible to window scripting on the Mac, so click them by position in a picture (M). A thing that will not select is usually the filter | `Ctrl+G` | Properties name it; filter restored |
| Move a block | Selection Filter to Footprints, drag left to right round the parts (right to left takes everything touched: 6 against 19 items, M), `M`, move, click: they moved together, 0.013 mm from the aim, and tracks stayed behind (M) | | Each part; ratsnest |
| Align, group | Select the parts, right-click near the top of the screen, Align/Distribute > Align to Top, or Grouping > Group Items (M). It aligned top edges and tracks stayed behind. The menu is tall: from the bottom of the screen only 3 rows showed, and typed keys reached the editor as hotkeys (M failed) | | Equal gaps visible; `(group` in the saved file |
| Measure | Coordinates from the file (M) | `Ctrl+Shift+M`, two clicks, `Esc` (M) (W). Or pointer on the start, `Space`, then read dx, dy in the status bar at the end (M). With grid snap off it read 2.006 for a 2.000 aim; with it on, 12.5 for a 12.7 pitch (M) | Axes measured separately |
| Fit, 3D | Mac: View > Zoom to Fit (M); PC: `Home` (W). 3D: `Alt+3` (M) (W), `Ctrl+W` closes it | | Whole outline |
| Dim other layers | `H` cycles them on the Mac (M) | Appearance panel | Put it back before judging |
| Refill, save | Edit > Fill All Zones (M); `Ctrl+S` (M) (W) | | Title has no `*` |

On Windows, selecting a footprint with the Footprints-only filter, `G`, arrow keys and `Enter` moved it with centered tracks attached with grid snap Never and Always (W). With snap Never, a displayed 0.5 mm grid and zoom 9.24, two Up presses during `G` moved the reported cursor about 0.5134 mm each; read the coordinates rather than assuming exact steps.

## What experienced designers do

Advice from KiCad forums and PCB design discussions, gathered in August 2026; not tested here.

- Start from the enclosure, mounting, controls and connectors; then the functional
  blocks, each arranged on its own, then bring the blocks together.
- Routing pain usually means weak placement. A routed board is no evidence that the
  placement was good.
- Decoupling capacitors at their power pins, with short returns and nearby ground vias.
- Good function is what looks good: short paths, few vias, consistent spacing and
  orientation. Tidying never overrides power, return paths or a datasheet.
- A first connected route is not the product: redo a local area that does not read cleanly.

## After every batch

Check pin 1, polarity, access and the actual enclosure.

## Recover

- A move on the cursor: `Esc` (M) (W). In the editor: `Ctrl+Z` one step at a time,
  looking after each (M) (W). File > Revert, then `Enter`, drops every unsaved
  edit (M) (W).
- Undo leaves the title's `*`: compare with the saved file, not the title.
- In KiCad 10.0.8, undoing a footprint move regenerated that footprint's Reference, Value, Datasheet and Description UUIDs on a disposable board, with or without an intermediate save (W). A no-edit save preserved them. On the Mac, the Reference field's live UUID changed immediately after undo, before any save (M). Recheck field IDs after undo; restored geometry alone is not a byte-identical restore.
