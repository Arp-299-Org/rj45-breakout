# Project tools: where KiCad work happens

The board's files are the ones `board/board.json` names
(`py -3 scripts/board_description.py` prints them); the KiCad machine's
folders are the ones `tools/board_graph_site.json` names
(`py -3 scripts/site_settings.py`). Below, `<checkout>` is the site settings'
`checkout` and `<prefix>` its `worktree_prefix`.

## Which checkout

On the Mac each branch has its own worktree beside the main checkout,
`<prefix><name>`:

```bash
py -3 scripts/mac.py run "git fetch -q origin && git worktree add -b <branch> <prefix><name> origin/main"
```

For a branch that already exists, `git worktree add <prefix><name> <branch>`.
Commit and push from that worktree, and open its files from there.

`<checkout>` stays on `main`. A push to main keeps it level with GitHub: the
pusher's `scripts/mac.py sync` (or a sync workflow) runs
`scripts/mac_keep_pace.py`, which fetches and fast-forwards main, then reloads
an editor that has a changed board or schematic open, and retries a refused
reload on later runs. It changes no file, and says why, when the checkout is
off main or holds commits GitHub lacks, a git operation is in progress, a
tracked file has uncommitted changes, or the incoming commits change a file
KiCad has open and it cannot see that KiCad holds no unsaved edits.

The board checks run in the branch's worktree:
`py -3 scripts/mac.py run "cd <prefix><name> && python3 scripts/validate_board.py --out /tmp/validate-<name> --base origin/main"`.

## Reloading

- An editor `mac.py open` started: File > Revert
  (`mac.py menu <pid> File Revert`, then `keys <pid> return` to confirm). It
  discards unsaved edits without asking.
- Any other reload: `scripts/kicad_reload_board.py` through
  `scripts/kicad_run.ps1 -Mode Live` on the Mac. It prints
  `status=reloaded` (exit 0) only when the editor matches the file item by
  item; `status=refused` (exit 2) changed nothing, and
  `status=verification_failed` (exit 3) means look.

## Checks after the work

- Before the first KiCad script of a session, run
  `scripts/kicad_preflight.ps1 -Project board -Mode Live` (or `-Mode Offline`
  for file-only work). Run KiCad Python scripts through `scripts/kicad_run.ps1`,
  never bare `python`. A project script is registered with its modes in
  `scripts/kicad-script-modes.project.json`; the tool's own scripts are in
  `scripts/kicad-script-modes.json`, which changes only in the tool's
  repository. Scripts must run on Python 3.9 (the Mac's KiCad Python).
  `scripts/setup_kicad_ipc.ps1` installs dependencies, is never run as a
  probe, and needs the approval any dependency change needs.
- `tools/kicad/create_disposable_project_copy.py` copies the whole project
  folder and renames `.kicad_dru` with the project. Models outside the project
  folder are not copied: judge 3D on the real board or on a copy that keeps
  them reachable.
- Copy a board to the temp folder before loading it in a script while an
  editor holds it, or the lock file can hang the load.
- `scripts/kicad_route_elegance.py --board <pcb>`, through
  `scripts/kicad_run.ps1 -Mode Offline`, is advisory: fix an unnecessary
  detour, corner or neck, and record the rest.
- Reports that will be cited are stamped with
  `scripts/kicad_report_freshness.py stamp` against the board they describe,
  and written with each tool's `--output` flag, never by redirecting stdout:
  the summary a tool prints and the file it writes are not the same document.

## Looking

Render after every board change: `tools/kicad/render_board_views.py`
(per-layer PDFs rasterized, no-pour views on a zones-stripped copy, 3D top and
bottom) and, for the schematic, `tools/kicad/render_schematic_pages.py` (PDF to
PNG overview and block crops). Open the PNGs with the Read tool, full frame
first and then crops of every region that changed. Do not export SVG for
looking; a dense sheet makes a file no viewer here renders reliably.

## Traps

- **A schematic generator.** If a script wrote the schematic, running it again
  after an edit made in the editor redraws the sheet and loses that edit. The
  first KiCad save of a generated file rewrites its format: commit that save
  alone so later diffs are readable.
- **DRC checks a project turns off.** Read the project's rule severities: if
  `track_not_centered_on_via` is off, a track that ends off a via's center
  passes DRC, so compare track endpoints with via centers explicitly.
- **The editor's socket can vanish.** After a night with a second Schematic
  Editor open, `api.sock` was gone and a Live job failed with "Connection
  refused"; restarting the PCB Editor brought it back.
- **Plan one change at a time.** Changes planned in parallel against the same
  board state collide, because none of them can see the others.

## Hybrid tools

`scripts/kicad_sexp.py` parses saved KiCad s-expressions;
`tools/kicad/kicad_semantic_snapshot.py` reads a semantic snapshot of the open
board when IPC use is in scope. The main-editor IPC refill helper is
`scripts/kicad_refill_zones.py`.

`scripts/kicad_hover_key.py <pid> '[[x, y, "e"], ...]'` hovers board positions
in the open Mac editor with the route tool's own window mapping, proves each
from the status bar and presses a key there; `--zones` lists the live board's
zones and rule areas over IPC, and `scripts/kicad_edit.py list --net NET --box
X0 Y0 X1 Y1` its copper, so a typed-coordinate edit is checked at once (M).

`scripts/kicad_route.py` drives KiCad's router but uses IPC for selection,
layers and optional save. It is hybrid and does not apply to GUI-only work;
its docstring gives the usage. It checks nets, frames the view, proves each
hover from the status bar and prints one JSON result (M). Read its `picture`;
confirm `closed` and the saved file. Any other `status` is a stop and its
`reason` explains it. `vias_at` reports where the router actually put vias.
`via_missed` means it got stuck far short and undid the route: add
`--through` corners or request a reachable via. Every call routes in Walk
Around unless it asks `--mode shove`; `router_mode` on every result says which
it routed in (M). A click lands up to about 0.02 mm off, so the tool takes tiny
jogs (segments under 0.05 mm) out over IPC and reports `trued_up` when it did.
`@X,Y` in place of the target pad ends the route on a via's centre or a
track's end of the start pad's net; `via@X,Y` ends it on a new via there, and
only a design check after a refill says it reached the plane. A part with
several pads of one number needs `REF.N@X,Y`. It needs the screen and a window
on top; for several PCB Editors use `--pid`. A stop undoes its copper but the
title may keep `*`: File > Revert or save.

`scripts/kicad_edit.py` makes exact edits in the open Mac editor over IPC,
where the router is the wrong tool: `list` a net's tracks, arcs and vias (or
`--texts`) with their ids, `delete` tracks and vias by id, `move-via` with the
track ends stored at its point, and `move-text`. Each edit is one commit, so
one Cmd+Z takes it back, and it reads the board back and prints one JSON
result with before and after; `ok` false means the read-back disagreed. It
never saves, creates copper or moves a footprint.

### A small edit, watched

A track or two that one agent lays and looks at itself does not need the step
runner; `scripts/routing_run.py` is for a batch nobody watches. On the board's
branch, in the Mac's worktree of that branch:

1. Take the shared editor (`mkdir <editor_lock>`, the site settings' lock),
   then `scripts/mac.py open <board>`, which prints the editor's pid.
2. `kicad_edit.py --pid PID list` the net and `delete` the old pieces by id,
   then `kicad_route.py PAD TARGET --net NET --pid PID`. Look after each
   change: `scripts/mac.py look "PCB Editor"`.
3. `scripts/mac.py keys pcbnew b` refills the pours and `cmd+s` saves; the
   title loses its `*`. `scripts/mac.py quit PID`, and remove the lock.
4. On the saved file: the design check with schematic parity (0 open, 0
   findings, 0 parity), route quality, `tools/kicad/check_track_craft.py`,
   and a comparison with the file before: only copper on the nets worked on
   may differ.
5. Bring the file into the branch's checkout, commit and record.

What this taught: a route starts at a pad, never at a via or a track's end.
KiCad's router does not finish in line with a track's end: come onto the end
at an angle (M). A `--through` point where the router would make its own 45
degree corner leaves a micro jog: put it on the straight run. The tool lays
the net class's width, so a neck is set afterwards in the Properties panel
(select the piece, `E`) (M). Run the routing-rules checker before a merge is
asked for: it is the one check that looks at how a track enters its pad.

A guarded schematic edit starts from a saved, committed schematic with no
unsaved editor, names the change, checks the file's hash and stops unless it
finds exactly that source.

## Full-file recovery

Outside GUI-only work, `git -C <prefix><name> checkout -- <pcb>` (or the
schematic) restores the whole file from the index (M); then File > Revert in
its editor. Check both states first: this discards every change to that file,
saved and unsaved.
