# Recipe: schematic

Work on the actual project's schematic and libraries, using the project's rules
and applicable checks. If the schematic is generated, identify how edits will
survive regeneration before changing it.

## Editor actions

| Job | Editor action | Verify with |
|---|---|---|
| Read a symbol, pin, field or position | Find `Ctrl+F`, type, `Enter` (M): the search also stops on note text. `Ctrl+G` shows all objects | Inspect the intended item. A saved file can be stale when the title has `*` |
| Read connectivity | Highlight a net with backtick; clear with `~` | Check the intended pins and net; a netlist from the saved schematic is another read-only check when permitted |
| Change fields, values or labels | Pointer on the symbol, `E` opens properties (M); change the field and confirm. Repeat on each item | Inspect the fields and affected connectivity |
| Move a symbol | Pointer on it: `G` keeps its wires (M) (W); `M` leaves them. Move the pointer, click to drop | Wire ends on pins; no dangling-end circle |
| Rotate or mirror | `R`, `X` (M): in the trial wires stayed where they were, so reconnect or undo. `Y` on the hovered symbol (M); or `E` | Pin flow; fields do not overlap |
| Add a symbol or power symbol | In a Mac trial, keys initially went to the hierarchy panel and `A` did nothing (M failed); click the empty canvas first. `A`, type `Device:R`, `Enter`, move, click, `Esc` `Esc`: one symbol added (M). One project-library filter returned no results (M failed). `P`, type `GND`, `Enter`, click (M) | Reference, value and footprint field |
| Wire | Pointer on the start, `W` (M) (W), move, click corners, end with one click on a pin, wire or label (M), `Esc`; `Shift+Space` cycles the angle | ERC and saved file: `Enter` and `K` in open space left no wire in a trial (M failed) |
| Label or global label | Pointer on the wire end, `L` (M) (W), type, `Enter`, click; `Ctrl+L`, the same (M) | Check attachment, ERC `label_dangling` and the netlist |
| No-connect or junction | `Q` drops one at the pointer; an extra click made a second (M). `J` (M): none was added in open space or on a plain wire (M failed) | Saved file |
| Fit | Mac: View > Zoom to Fit (M); Windows: `Ctrl+Home` (W) | Whole sheet visible |
| Save | `Ctrl+S` (M) (W), or File > Save | Title has no `*` |
| ERC | Inspect > Electrical Rules Checker, Run ERC (M) (W). In one Mac trial, unticked Show boxes listed Violations (0) while badges showed errors and warnings; tick the boxes and inspect the markers (M) | Findings and exclusions under the actual project's rules; compare with a suitable baseline |
| Plot | File > Plot opens (M) | Inspect the actual output, including each changed block |
| Update the board | When the task includes it: `F8` from the project manager (machine controls say how to open it) (M) (W). Read Changes To Be Applied, click Update PCB, read the log, Close and save the board. The first F8 after a script placed parts also writes unit metadata: read the list | Only intended changes; then inspect placement |

## Look and check

After a batch, check the whole sheet and each changed block against the
readability checklist: rule 1 of `.claude/agents/schematic-critic.md`.

Use the actual project's ERC settings and applicable checks. Compare findings
and affected connectivity against the appropriate baseline; changes to labels,
net names or pin names can change electrical meaning. When permitted, KiCad's
CLI `sch erc` (M) (W), `sch export netlist` (M), `sch export pdf` (M) and
`sch export bom` (M) were used in recorded trials. Choose the actual target and
launch method for the project. Read the report or output rather than relying
on a clean count alone.

## Recover

- In the editor, `Esc`, then `Ctrl+Z` one step at a time, looking after each
  (M). File > Revert, then `Enter`, drops every unsaved edit (M) (W).
- If undo would reverse work to keep, repair manually in the editor if possible;
  otherwise preserve the state and report the limitation.
- If a dialog is in the way, look at the whole screen, then `Esc`. Never
  force-quit an editor holding edits you did not make.
