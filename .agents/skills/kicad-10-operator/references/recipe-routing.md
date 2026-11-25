# Recipe: routing

Work on the identified project and use its actual layer stack, design rules,
net classes and approved placement. Inspect before and after; compare
connectivity, geometry and DRC against that project's baseline.

| Job | Editor action | Alternative | Verify with |
|---|---|---|---|
| First: every part on the board | Inspect the whole board and its outline | Compare footprint coordinates to `Edge.Cuts` in the saved file (M) | None unintentionally outside the outline; a mixer fixture had 19 parts off-board (M) |
| Read what is open | Ratsnest and Unrouted in the bottom bar (M) | DRC `unconnected_items`, when the task permits the check (M) (W) | The report matches the saved board |
| Read a net, its pads and endpoints | Hover, backtick: net name and length in the bottom bar (M), clear `~` | Inspect the saved file when permitted | Net name and coordinates |
| Route one connection, by hand | Pointer on the pad, `X` (M) (W), read net, layer, width, clearance and mode in the bottom bar, move, click corners, one click on the target pad ends it, `Esc` `Esc` (M) (W). `End` with the pointer on the target ends it too, and `F` from 70% of the way finished the route to its pad: each 0 open, 0 errors (M). From a selected pad: `Shift+X` (M) | Route > Route Single Track | Ends on pad centers, Unrouted drops by one |
| A pad under other items | Click the pad, read the chooser, `Esc` without moving the pointer, `X` (M) (W) | Selection Filter | Bottom bar names the net |
| Via while routing | `V`, click to place it: the router switches to the paired layer and continues (M). Read the layer before finishing | If routing ends, start again from the via with `X` (M) | Saved file: via, both legs and return path. `V` uses the netclass via without warning, even under an earlier Mac fixture's minimum (0.6 against 1.5 mm, M): compare them before routing |
| Corners | `Backspace` takes back a segment (M); `/` posture changed the route from 2 segments to 3, 0 open (M); `Ctrl+/` corner mode made 5 segments and left 1 open (M failed) | | The project's intended corner style, no needless corner |
| Width | `X` from a track takes that track's width (M). From a pad: read it in the bottom bar; 0.3 mm with the netclass at 0.2 and board minimum at 0.3 in one fixture (M). `W`, `Shift+W` changed nothing on that board at 0.2 mm (M failed). `Q` opens Track and Via Dimensions (M) | Edit track properties | Neck-downs deliberate |
| Router mode | Route > Interactive Router Settings… can change mode during an active route (M); `Ctrl+<`: Walk Around, Shove, Highlight Collisions (W). Put it back after: it stays set (M) | | Bottom bar names the mode. Highlight Collisions: with Allow DRC violations off, the Mac would not fix a track or via across another net (M); the PC fixed a via stub that shorted two nets (W). DRC after every route |
| Dirty start | "The routing start point violates DRC" (M) (W): seen on pads overlapping another net's; a pad next to its neighbour was allowed (M). Clear the violation, or start from the other end | | |
| Repeated channels | Tools > Multi-Channel > Repeat Layout was run with an IPC-selected source rule area (M); a fully GUI-selected source was not tested. Each target outline must match the source: one stretched to stray parts threw a channel off-board while reporting success (M) | `X` by hand | Look at every channel and the open list; tracks outside the area were clipped (M) |
| Change tracks (width, net, exact ends) | Edit > Edit Track & Via Properties…; `E` on one opens Track & Via Properties with typed Start X/Y, End X/Y and width, and on a via a typed position: double-click a field, type, OK (M, six edits on one supply net). Where two items share the spot KiCad lists them with their lengths: press the number (M) | | Width, ends and net in the saved file, read back over IPC |
| Drag a track | Hover, `D`, move, click, `Esc` (M). In one test it kept both ends connected (M) (W) | Delete and reroute | Check both ends and length; `G` can disconnect an end. Compare Unrouted and DRC |
| Drag a via | Hover, `D`, move, click, `Esc` (M). Its outer-layer tracks followed in one test (M) (W) | Delete and reroute | Check position and both sides for loose ends or hidden kinks; `G` can miss the target. Refill and inspect inner planes, then compare DRC |
| Delete | Mac: hover, `Backspace` or `Shift+Backspace` deletes one segment, not the track (M). Inside a via's ring the hover takes the via, not the track under it: untick Vias in the Selection Filter first, then tick it again (M). PC: click it, `Delete` (W); `Backspace` on a hovered track did nothing (W failed). `U` selects it first (M) | | Bottom bar's Segments and Unrouted; a dangling end can still be a live route |
| Rip up one net | Right-click a verified track > Select > Select All Tracks in Net; check the selected net, types and count, then `Backspace` (M: four two-pad nets, including F.Cu and B.Cu tracks and vias). Selection Filter: All items and all types checked, Locked items unchecked | | Refill, save and compare removed copper, other objects, opens and DRC with the baseline |
| Center the view | `F4` centers the view on the pointer (M) | | The intended area is visible |
| See a layer | `PgUp`, `PgDn` (M) (W); `H` cycles the rest on the Mac (M) | Appearance panel | Inspect relevant copper layers |
| Refill, save | Edit > Fill All Zones (M); `B` (W); `Ctrl+S` (M) (W) | | Title has no `*` |

## When a route is blocked

If local attempts keep stopping in the same corridor, change the route plan.
Inspect both layers at the proposed via and each endpoint's escape. An escape
away from the destination can reach open space. Plan nearby connections
together: reversed pin order may need a layer crossing or a path around an
endpoint.

Use the current preview and clearances to adjust reference waypoints. If a
fixed corner traps the next leg against an obstacle, `Backspace` takes it back
so it can be placed elsewhere (M).

If an existing route occupies the needed space, identify its endpoints and
branches, then rip up the connection you will rebuild. The whole-net action
above was tested on two-pad nets; account for every branch before using it on
a larger net. Route the constrained connection first, then restore the removed
one. Compare the saved changes and expected opens after rip-up, and check all
affected nets after rerouting.

## Track and via drag

- `D` on a track, snap Never, Walk Around: it added bends and length while
  keeping both endpoints, the via and the other layer's track fixed; DRC
  matched the baseline (M) (W). Off-center pointer movement gave a different
  displacement: measure the saved geometry.
- `D` can fall short: a 2 mm request stopped at 0.11 mm against copper in its
  way (M), and a 0.15 mm request moved nothing once (M failed, not retried,
  so no general limit). `G` moved nothing
  on a ground track twice where `D` moved it (M failed). An exact connected
  GUI-only shift that small is not established: check actual geometry.
- `G` on a track detached the pad end when started near the middle (M) (W),
  and the via end when started near the via (M), with either selection
  filter. DRC found the loose end and the missing connection.
- `D` on a via, snap Never, Walk Around: it moved off-grid and its outer
  tracks followed (M) (W); inner-plane clearances stayed at the old position
  until refill (M), so a stale fill reports false clearance errors after a
  via moves. A `G` preview moved both tracks, but the placed via went back to
  its start and the saved board was unchanged (M) (W); a smaller `G` moved it
  sideways (M). The causes are unknown.

## Routing and vias

- `V` and click can end the route (M): start again at the via with `X` and
  click the target on its layer; finishing on a pad on the other layer left
  one open (M failed). `PgDn` or `PgUp` selects an outer layer (M) (W). `V`
  again then `Esc` `Esc` left no copper (M).
- On Windows, `V` then `Enter` placed a through-via, switched F.Cu to B.Cu and
  kept routing; leaving with the selection arrow kept the via and the front
  segments, including a short jog, and one undo restored the saved board (W).
  Inspect the via, the layer and short segments.
- A blocked via attempt committed its lead segments with no via (M): `Esc` is
  not an all-or-nothing rollback. Inspect the saved via, its legs and any
  leftover copper, including short segments inside a via that DRC may not
  flag. A redundant spur and a serial segment joining the route to the via
  center look alike; keep the serial ones. To remove a spur: hide vias,
  select Tracks only, zoom in, check the segment's start and end in
  Properties, delete it, and restore the selection filter (M).
- Route > Set Layer Pair chose an outer and an inner layer; `V` continued on
  the inner layer, and a second via returned to the outer layer and closed the
  connection (M). Reopening reset the pair to Top/Bottom: recheck it. Inspect
  short segments and both refilled planes.
- With grid snap Always and magnetic snap on, `X` started at the pad center,
  not the grid cursor's coordinates (W): verify the actual start. Canceling an
  unfixed preview with the selection arrow left no saved change (W).
- A detour to a same-net pad on the other layer closed the net but left the
  old branch dangling: zero Unrouted, yet a DRC dangling-end finding (W).
  Inspect old branches and short segments, check ignored DRC tests, and
  compare track endpoints with via centers explicitly.
- Nets whose names end in N and P (such as CPN and CPP) are read as a
  differential pair, so "use netclass width" gave the pair width: set the
  width with `Q` (M).
- Place Vias snaps to tracks and pad centres, not the click: two vias in one
  pad landed 0.1994 mm apart, hole to hole. Move one with `E` and typed
  coordinates (M).
- Walk Around drew the wrong way round a chip when the pointer jumped to the
  target in one move: move it in steps (M).
- `X` once started a route at an old pointer position: read the pointer
  position before pressing `X`; `Esc` `Esc` left no copper (M).
- Hand-clicked corners can land a few micrometres off-axis and leave a jog (M).

## After every batch

- Look for vanished or fragmented pours: in one test a band of F.Cu ground
  was gone and DRC did not report it (M).
- After Shove, inspect the full paths of changed neighbours, power tracks
  included: one repair substantially lengthened an analog-supply path with
  no new DRC finding. Undoing it and routing from the other endpoint in Walk
  Around avoided moving the supply (M).
- Shove recreated UUIDs on geometrically unchanged long segments (M): compare
  geometry and connectivity to tell these replacements from moved copper.

## Checks after

Refill in the editor and compare applicable DRC findings and unconnected
items with the project baseline. Inspect affected copper and planes; DRC
alone does not establish path quality or return-current behavior. For DRC
project context, exclusions and permitted CLI checks, read
[the finish recipe](recipe-finish.md).

A dangling stub can still be a live run through a via; compare the prior
board before deleting it. Hole clearance is separate from netclass copper
clearance; non-plated mounting holes are obstacles too. Rebuilding a whole
chain can silently re-lay every segment. In one case, 0.05-0.15 mm shifts
on a long run consumed real clearance: re-run DRC after geometry cleanup.

## Recover

- In the router: `Backspace` a segment (M), `Esc` the unfixed part, a second `Esc` leaves
  (M) (W).
- `Ctrl+Z` one step, then look (M). In the tested saved-reroute cases, undo
  and save restored the deleted-state board byte for byte (M) (W). Undoing a
  footprint move changed field UUIDs in another Windows case (W), so inspect
  the saved result. File > Revert, `Enter` drops all unsaved edits (M) (W).
- If undo would also reverse work to keep, repair manually in the editor if
  possible; otherwise preserve the state and report the limitation.
