# Agent instructions

Every agent reads this file first. Rules that bind every agent go here, never
in one agent's private memory. Fill in the product section; keep the rest
unless the owner changes it.

## Product

A compact passive RJ45 (8P8C) to 2.54 mm pin header breakout board for
breadboarding and workbench probing. Work fails if pin numbering or silkscreen
labels are ambiguous, RJ45 mounting tabs lack mechanical stability, or signals
short or mis-map between the jack and header. `docs/PRODUCT_TRUTH.md` holds the
full statement (draft awaiting owner confirmation on the `Decisions` card).

## The owner

The owner's words in chat outrank every doc. The owner decides product
behavior, architecture, parts, placement, cost, purchases and tradeoffs:
bring those choices with a recommendation and its reason, so the answer is
yes or no. "Go" or "fix" authorizes the agreed step, not a new scope, part,
purchase or unattended run. A question, brainstorm or audit is not permission
to edit. Record a decision only after the owner adopts it, in the owner's
words, on main the day it is made.

## Honesty

Keep apart what was planned, attempted, observed, inferred and verified. A
check proves only what it measured; a passing build, DRC, ERC or critic is
evidence for that property, not product success. Say when a tool stopped,
evidence is missing, or steps are being repeated. When you notice something
wrong while doing something else, say so with the file and line.

## Board workflow

- **Graph.** Board work is on the graph (`tools/board_graph.json`), never
  beside it. A session that touches the board starts with `board-graph where`,
  starts the card it names with `next --by <who>`, does that card and nothing
  else, and ends with `record`.
  In a repository with several boards, `where` shows them all and every
  other command names its board: `--board <name>`.
  Work the graph has no card for is first a change to the graph, brought to
  the owner. `docs/BOARD_PIPELINE_CONTRACT.md` says how the graph runs.
- **A card that does not work.** When a card's script or tool fails or
  refuses, stop. Record `needs_lead` with what it said, word for word, and
  tell the owner in plain words what failed. Never do the card's work another
  way, with another tool or by hand, and never record it as done. Never
  propose a replacement for a tool the owner chose (another router, a script
  in its place). Say what was done by its true name: copper a script wrote
  is not "routed by hand". Never write a note or a memory that tells a later
  session to avoid a card or its tool.
- **Copper.** Copper is laid only by the Routing batch card's routing run, in the
  locked KiCad editor, using the task's authorized mode (`Mode: ipc`,
  `Mode: hybrid` default, or `Mode: interactive`): checked atomic IPC chunks via
  `scripts/kicad_lay.py`, and/or KiCad's interactive router via
  `scripts/kicad_route.py` (`--mode shove` / GUI). Ad-hoc scripts or
  wrappers (`wrapper_calls`), raw `create_items`, direct `.kicad_pcb` edits,
  and unauthorized external autorouters remain forbidden. Report the mode and
  solver provenance honestly in receipts; only the owner's own record accepts
  copper laid outside a run. If the run fails, stop and report it.
- **Opus is banned from routing.** An Opus model does not route, start the
  routing run or record on the Routing batch card: it says so and stops. The
  routing run refuses an Opus model as its agent or its reviewer.
- **Board.** The schematic is the source; the board is updated from it, never
  changed behind it. Never route ahead of placement the owner approved on a
  rendered view; placement settles position, rotation and side. After every
  batch of edits, export a picture, look at it, and fix what looks wrong; the
  owner's eyes are never the first look.
- **Parts.** Adding or changing a part means getting its datasheet into the
  datasheets folder, taking its specs from it, and making or checking its 3D
  model against them. The footprint library stays identical to the board and
  holds nothing else.
- **KiCad.** One board file and one writer. Save any unsaved edits in the
  open editor before a change, apply the change on top, and reload the editor
  after. Never run KiCad's Python directly from a tool on a machine where it
  opens a window; KiCad's command-line tool runs through
  `tools/kicad/invoke_kicad_cli.py`.
- **Tool files.** `board-graph` runs from its installed package or shared
  checkout (and `kicad_machine.tool_checkout` on a separate KiCad machine), so
  a project repository holds only project files (`board/`, `tools/board_graph.json`,
  `tools/board_graph_site.json`, records, docs, and starter config). Change tool
  code in the `board-graph` repository, never inside a board repository.
- **Git.** Before editing, check the checkout matches its branch on GitHub.
  Board changes go on a branch and a pull request. No attribution footers or
  co-author trailers in commits.

## Writing

Plain words, short sentences, tables for comparisons. Name a part by what it
is and its reference: "the power jack (J1)", never a bare J1. Docs say what
is true now; git keeps the past. Keep code `#` comments to non-obvious
invariants, KiCad/OS quirks, and fail-closed reasons; never write dated
diary entries, owner chat transcripts, or comments that restate the code.

## Where things live

`docs/PRODUCT_TRUTH.md` first. Board: `board/board.json` (the board's files),
`board/DECISIONS.md`, `board/SPACE.md`, `board/ELECTRICAL_AUDIT_CONTRACT.md`,
`board/ORDER_PACKAGE_CONTRACT.md`, `docs/BOARD_ORDER_COMMON_SENSE_CHECKLIST.md`.
Routing: `docs/ROUTING_NOTES.md`. KiCad: `.agents/skills/kicad-10-operator/`.
Critics: `.claude/agents/board-critic.md`, `schematic-critic.md` and
`.agents/critics.md`, with the same two for Codex in `.codex/agents/`.
Machine settings: `tools/board_graph_site.json`.
