---
name: kicad-10-operator
description: "Use to inspect or operate KiCad 10 schematic and PCB editors, including placement, routing, vias, zones, ERC, DRC, and GUI-only or explicitly permitted hybrid workflows. Adapt the instructions and checks to the actual project. Does not decide circuit or product requirements."
---

# KiCad 10 operator

Identify the actual project and its board, schematic, rules, libraries and
layer stack before operating. Use its requirements and checks; do not assume
another project's filenames, net names, waivers or validation apply.

Follow the owner's chosen workflow. For GUI-only work, make changes, refill,
save and recover through the real editor. Do not use IPC, `pcbnew`, CLI or
offline edits to mutate the design. Read-only saved-file inspection and checks
are available when the task permits them. Otherwise, choose a suitable route
and pair it with checks for what it misses.

Read the stage recipe needed for the work:

| Stage | Recipe |
|---|---|
| Schematic | [recipe-schematic.md](references/recipe-schematic.md) |
| Placement | [recipe-placement.md](references/recipe-placement.md) |
| Routing | [recipe-routing.md](references/recipe-routing.md) |
| Finish | [recipe-finish.md](references/recipe-finish.md) |

For this project's checkouts, reloads, checks and the board graph tool's
KiCad scripts, also read [project tools](references/project-tools.md). For
the Windows PC and the Mac that runs KiCad, read
[machine controls](references/machine-controls.md). Read
[hybrid operation](references/hybrid-operation.md) only when that workflow is
within the owner's chosen scope.

`(M)` and `(W)` mark gestures practiced on the Mac and on Windows, and failed
trials are marked; unmarked ones were not recorded as practiced on either.
They are this workspace's fixtures, not a guarantee that another project
behaves the same way. `Ctrl+F1` lists the editor's hotkeys (M). KiCad 10
manuals: https://docs.kicad.org/10.0/en/pcbnew/pcbnew.html and
https://docs.kicad.org/10.0/en/eeschema/eeschema.html.

One agent at a time on a desktop: another session's command can take the
front between two of yours. Before opening an editor on a file, check the
open windows and its lock file (`~<file>.lck` beside it). Re-observe
whenever the project, window, item, net, layer or tool is uncertain.

After every batch, whatever the route, inspect the exact result in the real
editor and in the saved file; a later change invalidates that look. A
preview or a clean DRC count alone does not prove the intended copper is
present or the return path is good: compare affected geometry, connectivity
and checks with a baseline. Save, close and reopen when persistence matters.

A gesture is practiced on a machine when a recipe records it as practiced
there; reading the manual or the installed interface does not make it
practiced. Say at once when an operation is unfamiliar, unreliable or not
practiced on the machine at hand. A mutating gesture not yet practiced there
is first rehearsed once on a uniquely named disposable copy
(`tools/kicad/create_disposable_project_copy.py`): do it, inspect the
result, confirm the recovery path and record it in its recipe, then do it
on the real files.
