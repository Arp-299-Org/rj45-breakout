# Machine controls for this workspace

These controls describe a Windows PC and the Mac that runs KiCad, the
setup the board graph tool assumes today; they do not select or validate a
design project. `mac.py run` starts in the checkout the site settings
(`tools/board_graph_site.json`) name; resolve the utility and design paths
separately.

## Windows and macOS

These are the installed workspace controls, not a default project. KiCad
locations are in `tools/kicad/kicad_install.py`; the workspace also has
`scripts/kicad_*.ps1` runners (PowerShell 7 on both machines).

| | Windows PC | macOS KiCad machine (the site settings' `ssh_host`) |
|---|---|---|
| Hotkeys | As written in the references. | Cmd where KiCad says Ctrl, Option where it says Alt; single-letter tool keys are the same. |
| Live IPC mode | Yes. | Yes: `.venv-kicad-ipc/bin/python`; the preflight needs exactly one running KiCad app. |
| PyMuPDF for renders | `py -3` has it. | `python3` has it. |
| Hover hotkeys (practiced on each) | KiCad misses one pointer jump: move twice and wait first. | One `mouse move` and about 0.4 s was enough every time. |
| Wheel zoom (practiced on each) | One call is one step whatever the amount: repeat move, move, scroll. | The amount counts: 8 took the zoom from 2.94 to 5.95. Move once first: a scroll with no move since the editor opened zoomed at 0, 0. Zooming moves the point under the pointer to the canvas center and warps the pointer there, so mm to screen points is exact: about 3.585 x Z points per mm. Recentering is one step in, one step out. |
| Opening an editor from KiCad's manager (practiced on each) | Double-click the file row, looking first: a `.history` folder shifted the rows and a double-click hit `.kicad_dru`. One click on the Schematic Editor button did not open it within about 14 s. | All worked: the Tools menu, one click on the button (open within 7 s), a double-click on the file row. A `.history` folder did not show in the tree, but look first. |

## The Mac

The Mac locks after 300 s idle. `mac.py` reports no error while it is locked:
windows, window looks and mouse commands all still answer, and pid targeting can
pick the wrong editor when several are open. Start every run with a whole-screen
`mac.py look`, and stop if it shows the lock screen; only the owner can unlock it.
`mac.py run "ioreg -n Root -d1 -a | grep -A1 CGSSessionScreenIsLocked"` is a
read-only check that also catches the screensaver before the password field shows.
Close editors a run does not need before sending keys.

The Mac's checkout is kept level with GitHub by `py -3 scripts/mac.py sync --apply`,
which a session runs right after its push to main (the sync workflow does the
same on the Mac's runner for a merge made on GitHub); nothing polls.

SSH sees and drives the screen through macOS's Screen Recording and
Accessibility switches, which on macOS 27 are in System Settings under Device
Control and Data Access. When macOS
refuses, `mac.py` prints macOS's own message and stops:

| Message | Meaning |
|---|---|
| "could not create image from window" | The window closed or changed after it was listed: list again. |
| "could not create image from display" | SSH may not read the screen: the Screen Recording switch is off (macOS may ask again weekly). If it persists, tell the owner what macOS said. |
| "not allowed assistive access" | The Accessibility switch is off: tell the owner. |
| "Could not list the windows" | The session cannot reach the Mac's desktop at all. |

Any other failure is yours to diagnose first.

## Opening, looking, acting

`scripts/mac.py`'s docstring lists the commands. What it does not say:

- `open` also prints the new editor's window number and title: use the pid
  for `menu`, `keys` and `type`, and `#<n>` for `look`. Paths are relative to
  the Mac's checkout or absolute; `~` does not expand. A title or pid does not
  prove the full project path. On a disposable board, `Cmd+S` showed the full
  saved path in the bottom status line for about 4 seconds. Do not save an
  unidentified editor merely to learn its path; if the target stays
  ambiguous, stop.
- From Git Bash, set `MSYS_NO_PATHCONV=1` before an absolute Mac path such as
  `/tmp/...` or a net name such as `/NAME`, or Git Bash rewrites it into a
  Windows path. Give each nested heredoc sent over SSH its own delimiter, or
  the rest of it runs on the PC.
- `look "#<n>"` copies that one window even while others cover it and prints
  the picture's path: open it with the Read tool. It removes the old picture
  first, so a failed look never hands back an older one. Dialogs do not show
  in a look at one window: `look` with no name shows the whole screen.
- Menu names must match exactly, including KiCad's one-character ellipsis in
  "Save As…", "Interactive Router Settings…" and "Update PCB from
  Schematic…"; `menus <pid>` lists them.
- Keys go where the focus is: after the search field or a dialog, click the
  canvas first. A tool key (M, G, R, E, X, D) acts on the item under the
  pointer, so `mouse move <x> <y> --pic` first. Pass lowercase letters (`x`,
  `cmd+s`) and name Shift explicitly: the helper keeps the case, and `CMD+S`
  opened Save Board File As (M).
- `mouse click --pic` takes pixels of the last look, whichever it was: after
  a whole-screen look the same numbers land elsewhere. It does not prove
  which project is open or keep another session off the desktop. Move before
  a click while a tool is carrying something. `--count 2` double-clicks;
  dialog fields take a double-click before typing.

## Opening a project manager for F8

Tools > Update PCB from Schematic… (`F8`) needs the project opened in
KiCad's project manager: a stand-alone editor cannot update the board, and
`mac.py open` opens `.kicad_pcb` or `.kicad_sch`, not `.kicad_pro`. Launch
the explicitly named project, for example:

`py -3 scripts/mac.py run "open -n -a /Applications/KiCad/KiCad.app '/absolute/path/to/example.kicad_pro'"`

Replace the example with the actual project path. Use `mac.py windows` and
Tools > Schematic Editor before `F8`.
The manager and its editor windows share a PID; menu and key actions reach the
front one. F8 opens the PCB Editor too, and its dialog needs a whole-screen
look. In one Mac test selecting an item in one editor also selected and centered
it in the other. Close with `cmd+q` only when doing so is safe; `mac.py quit`
closes only a window it started.

## Windows computer use

In Codex Computer Use, a native KiCad dialog can appear in a separate screenshot within the editor state. A parent-window click or accessibility action may be rejected; use the dialog screenshot's own ID and coordinates, or navigate it by keyboard. This was observed on the Open Board and Preferences dialogs (W).

## The runner and IPC

`scripts/kicad_run.ps1` preflights its `-Project` but passes `--board` and
every other script argument through unchecked: make both name the intended
project. From `pwsh -File`, give each script argument as one word
(`-ScriptArgs --project=board`); an `@(...)` list works only from
`pwsh -Command` or inside PowerShell.

Identify the opened editor's actual IPC socket with
`lsof -U -a -p <pid> | grep /tmp/kicad`. A sole editor can own
`/tmp/kicad/api.sock`; do not assume `/tmp/kicad/api-<pid>.sock` exists.
Set `KICAD_API_SOCKET=ipc://<observed socket path>` for that process.
The guarded Live runner accepts the single-editor case and refuses conflicting
KiCad apps. With multiple editors, use the intended editor's menus or its
verified socket without bypassing the runner's checks for a Live job.
Check `board.document.board_filename` and `board.document.project.path`
before any write.
