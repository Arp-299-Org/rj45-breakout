# Routing notes

Read this before working on routing or the KiCad skill. The first part is how
the tool's routing works and what was learned building it; the last section
is this project's own, for what it tries and finds. Keep apart what was tried
and observed from what is still unfinished.

## The ways copper is laid

Copper reaches the board one way: the Routing batch card's routing run
(`board-graph route`, `scripts/routing_run.py`) driving the locked PCB Editor
under one of three declared modes (`Mode:` header in each task, defaulting to
`hybrid`):

- **`Mode: ipc`:** Checked atomic IPC laying via `scripts/kicad_lay.py`
  (`route`, `batch --json` / `--stdin`, `pads`) for clean open channels,
  parallel buses and straight joiner/trunk chunks where speed and exact
  geometry win. Pass batch JSON inline with `--json` or heredoc `--stdin`
  (never call `write_file` or create scratch files). Every `kicad_lay.py` commit
  snaps to pad centers, enforces `Pad exits: centered` before editing, checks
  45-degree geometry and live route quality, confirms connectivity, runs
  `kicad-cli` DRC diffing, and rolls back on any error.
- **`Mode: hybrid` (default):** Combines `scripts/kicad_lay.py` for clean
  runs with `scripts/kicad_route.py` (`--mode shove`) in dense spots within
  the same locked step.
- **`Mode: interactive`:** KiCad's interactive Push-and-Shove / Walk-Around
  router only (`scripts/kicad_route.py` and GUI `X`). Right for dense IC
  escapes and surgical rework inside existing copper.

Forbidden in all modes: ad-hoc scripts importing `kipy`/`pcbnew`/`kicad_lay`/
`kicad_route` (`wrapper_calls`), calling `create_items` outside `kicad_lay.py`,
editing `.kicad_pcb` directly, and unauthorized external autorouters. Receipts
record `routing_mode`, `lay` counts, and `route` counts truthfully (while
retaining legacy `autoroute` provenance on older receipts): IPC-laid copper
is recorded as such, never "routed by hand".

The graph holds this: the card refuses `pass` and `more_work`, and the board
checks fail, while the branch holds copper that no adopted run committed
(`scripts/board_copper_origin.py`). Only the owner's own record on the card
accepts copper laid another way.

Opus models are banned from routing: the run refuses one as its agent or its
reviewer, and adopts nothing from a run one did work in.

When the run cannot lay a connection, record `needs_lead` with what the tool
returned, word for word, and bring it to the owner. Do not bypass the locked run
or use another router.

## Planning when to use which mode

Plan the routing mode per task/chunk when authoring `tasks/` on the Routing
batch (and note batch method in Constraints):
- Use **`Mode: ipc`** (multi-`Connection:` chunks of clean buses/joiners) when
  paths are unobstructed and shoving is unneeded, turning ~30-90 s/wire GUI
  routing into ~1-2 s per chunk while keeping full DRC, pad-exit and cold review.
- Use **`Mode: hybrid`** when a chunk mixes clear runs with tight crossings or
  existing tracks nearby.
- Use **`Mode: interactive`** for dense fanout, tight shoving, or delicate rework.
- If an `ipc` chunk fails repeatedly with `drc_failed` or obstacle collisions,
  escalate that wire to `hybrid`/`interactive` (`--mode shove`) or stop cleanly
  with `needs_lead`.

## What was learned

Some earlier runs skipped the editor or recorded scripted copper as hand
routing. The owner also observed Codex completing editor skill work with
shell access. Skill development and a production Routing pass have different
acceptance checks. For a production pass, check the named connection in the
saved board, its origin in the interactive router, and the independent review.

On KiCad's mixer demo, runs without the skill passed DRC with 213 to 355
vias. KiCad's version had 29. Review the resulting layout as well as DRC.
In the editor, a popup, a locked screen, window focus or a corner snapping
to a pad can explain a missed gesture.

Earlier trials introduced the following changes together. The trials did
not isolate which changes each operator needed.

| Change | How |
|---|---|
| Limit each step | Name the pads on one net |
| Make it cheap | `scripts/kicad_route.py`: the agent names pads, and KiCad's own router does the work |
| Limit the routing operator's tools | The current routing subprocess locks the board file and disables the general shell. This describes that subprocess only. |
| Check the saved board | Check the connection, DRC, route quality and electrical audit. Preserve a qualifying candidate for an owner decision when quality warnings remain. Passing requires independent review. |

- **Details decide it.** Most failures had one small cause, found by zooming
  in on one net: KiCad's chooser asking "footprint or track?", a router mode
  nothing could reach, the pointer jumping to a part's center.

## How to use it

`scripts/kicad_lay.py` inspects pad centers/netclasses/facing edges (`pads`) and
lays checked 45-degree copper chunks atomically over IPC (`route`, `batch
--json` / `batch --stdin`), verifying centered exits, live route quality,
connectivity and `kicad-cli` DRC before committing (and rolling back on any
failure). `scripts/board_context.py` gives operators an offline world-coordinate,
courtyard, rule and copper brief (plus `routing_agent.plan` when configured) at
startup so IPC chunks need no discovery calls before planning. `scripts/kicad_route.py`
plans straight surface-mount pad escapes and guides KiCad's interactive router
inside the bends (`--mode shove` / Walk Around); it checks pad crossings and
route quality before committing and undoes a rejected route.
`scripts/kicad_edit.py` makes exact edits over IPC (list, delete, move a via
with its track ends, move a text) and never creates copper.

`scripts/editor_step.py` runs one task, or a folder of tasks one step each, in
one open editor on the KiCad machine, on a throwaway copy outside the
checkout, with that machine's screen unlocked; its docstring has the usage and
how a step passes. On the Routing batch card the lead does not run it by hand:
`scripts/routing_run.py` runs a committed folder of tasks through it, adopts
the board only when tracks, arcs and vias alone changed, and records the
outcome with the step lines and tokens.

Not finished in the tool: no agreed measure of a better route; `Mode: interactive`
GUI shoving (`scripts/kicad_route.py`) remains macOS-only (`Mode: ipc` runs on macOS and Linux + `Xvfb`).

## This project

What this board's routing tried, what was observed and what is open: each
batch's result and its cost, and each connection the run could not lay.
