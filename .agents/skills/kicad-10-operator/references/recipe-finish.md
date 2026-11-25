# Recipe: finish

Finish the identified board using its own rules, stack, output and review
requirements. Inspect the actual saved result.

| Job | Editor action | Alternative | Verify with |
|---|---|---|---|
| Read zones, silk, stack | Pointer on the item, `E` | Inspect the saved file when permitted | Title has no `*`, or the file is stale |
| Refill in the open editor | Edit > Fill All Zones (M); `B` (W) | | Each copper layer: thermals, islands, necks, pours and return paths |
| DRC | Inspect > Design Rules Checker (M) (W), parity box when available, Run DRC, Close. KiCad 10.0.8 hides parity in standalone editor mode (documented); it agreed with CLI in one test (M). **Check project exclusions before and after saving:** DRC and save rematch exclusions to markers, and drop footprint-library mismatch exclusions when that library is unavailable (M) (W); with the library, a match still depends on marker identity and location (M) | Applicable read-only DRC check if the task permits it | Fresh report; findings, unconnected, parity, ignored tests and exclusion changes |
| Fix a finding | The placement or routing recipe, where it lives | | DRC again |
| Draw or reshape a zone | Place > Draw Filled Zones (`Ctrl+Shift+Z` did nothing on the Mac, M failed), click the first corner, pick the net and layer, click OK (`Enter` did not close it), click the corners, double-click: 3 zones to 4, 0 errors (M); with no net picked the zone has none | | Net, layer, boundary, then refill |
| Silk: one reference off a pad or edge | Selection Filter: All items off, Text on, pointer on it, `M`, move, click: the text moved and the part did not, but not to the aim: 0.99, 0.82 for 1.0, 0 (M) | | Readable beside its part |
| Silk: many references, sizes | Edit > Edit Text & Graphics Properties… opens (M) | | Off pads and edges, both sides |
| See each layer | `PgUp`, `PgDn` (M) (W), Appearance panel for inner layers | Applicable layer export | Saved board |
| Both outer copper layers | Appearance with F.Cu and B.Cu on (W) | Applicable layer export | Known front-only and back-only features |
| Check enclosure fit | `Alt+3` (M) (W), `Ctrl+W` closes it | Applicable 3D render | Models, connectors and mechanical access |
| Statistics | Inspect > Show Board Statistics (M) (W) | Counts from the file; Pads, Vias, Segments, Unrouted in the bottom bar (M) | Compared with the project's limits |
| Fabrication outputs | Follow the project's approved ordering instructions | | Their own checks |
| Save, close, reopen | `Ctrl+S` (M) (W); `Ctrl+Q` (M), or close the window (W); reopen the same way | | Saved file hash unchanged after reopening in the tested cases (M) (W) |

For a multipage copper PDF, name the images by its layer bookmarks or page
labels: exports have come in more than one layer order (M).

## IPC reference text rehearsal

On the Mac with KiCad 10.0.8, updating a reference's parent footprint through
IPC changed only that reference's text size in a disposable project; saving,
undoing and saving restored the board byte for byte. A separate 90-degree
reference-text rotation changed only that field's angle, and undo and save
restored the disposable board byte for byte. Updating the Field object
alone returned the requested value but changed neither the live field nor the
saved file. Query the actual board after the commit and compare the saved file.
## Checks after

Run the identified project's applicable checks and compare them to the
baseline. Confirm the saved fills are current and inspect affected layers,
models, clearances and output files.

Keep the board with its matching project file and any project-named
`.kicad_dru` custom rules, and make its libraries available. Without the
associated rules KiCad can silently use defaults; unavailable libraries
also changed DRC and exclusion results in recorded tests (M) (W).

When the task permits CLI checks, the practiced command forms include
`pcb drc --format json --severity-all --schematic-parity --refill-zones`
and `pcb export pdf --layers F.Cu,B.Cu,Edge.Cuts --mode-single` (M), with
the actual board and output paths. Use schematic parity only when it applies
and the matching schematic is available.

**Refill before believing DRC.** A stale fill invents phantom errors, such as
vias shorting a ground pour at exactly 0.000 mm. `--refill-zones` refills in
memory, so it does not prove the saved fills are current; `--save-board`
writes the refilled board back, which changes the design (it left an
already-current fill unchanged in one test (M); a stale fill was not
tested). So refill in the editor (Edit > Fill All Zones) before every save
that changed copper or footprints.

## Recover

- `Ctrl+Z` one step at a time, looking after each (M). File > Revert, then
  `Enter`, drops every unsaved edit (M) (W).
- DRC dialog left open: look, then `Esc`. A refill that hangs the editor: look,
  wait, and if it never returns, report it before quitting anything.
