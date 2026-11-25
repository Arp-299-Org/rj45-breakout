# The board in 3D

Every position, height and direction in this repository uses these words.
Numbers below come from the saved board and its models. A model is evidence
about the model, not the part: confirm against a datasheet or calipers before
relying on one.

## Axes

| Axis | Direction | Range on the board |
|---|---|---|
| X | grows east | `0.0` to `36.0 mm` (`1.5 mm` corner fillet radius) |
| Y | grows south, as in KiCad | `0.0` to `35.0 mm` |
| Z | grows out of the front face | `1.6 mm` board thickness (`F.Cu` at `+1.6`, `B.Cu` at `0.0`) |

## Words

| Word | Means | Never means |
|---|---|---|
| Front face, back face | The board's two sides: F.Cu (+Z) and B.Cu (-Z) | An edge |
| North, south, east, west edge | The four board edges in KiCad's top view | A face |
| Height | Distance along Z from the face a part mounts on | Length or width in the board's plane |
| Thickness | The enclosure body's total along Z | A part's height |
| Overhang | How far a part passes a board edge, along X or Y | Height |

"Back", "top" and "bottom" alone are not used: "back" can mean a face or an
edge, and that ambiguity has caused errors before.

## In the user's hands

The board sits flat on a workbench or mounts on 4x M3 standoffs with the front face (`F.Cu`) pointing up (`+Z`). The north edge (`Y = 0`) is the RJ45 cable entry: the right-angle 8P8C jack (`J1`) is flush with the north edge so an Ethernet/patch cable plugs straight in from the north with latch-release tab on top (`+Z`). The south half carries the 1x8 2.54 mm vertical male pin header (`J2`) pointing straight up (`+Z`), with pin `1` (`W/O`) on the west end (`X = 9.11 mm`) through pin `8` (`Br`) on the east end (`X = 26.89 mm`), cleanly clear of all four M3 corner screw heads (`6.0 mm` keepout) for test clips, DuPont jumpers, or a 1x8 female harness.

## Where the parts sit

| Part | Face | In the plane | Height |
|---|---|---|---|
| RJ45 8P8C jack (`J1`, `MJ56881-B011-HLRN1-C`) | Front (`F.Cu`) | Centered at `(18.0, 6.475)` mm, `180 deg` (mating opening flush at north edge `Y = 0.0`, body `15.20 x 12.95 mm`, `2x Ø1.20 mm` locating pegs) | `12.50 mm` (datasheet p. 1) |
| 1x8 2.54 mm male header (`J2`, `HX PZ2.54-1x8P TP-ZQ`) | Front (`F.Cu`) | Centered at `(18.0, 25.0)` mm, `0 deg` (pin `1` west at `X = 9.11 mm` to pin `8` east at `X = 26.89 mm`) | `9.20 mm` (`3.20 mm` insulator + `6.00 mm` pin, datasheet p. 1) |
| Corner mounting holes (`H1`..`H4`, `3.2 mm` M3 NPTH) | Front (`F.Cu`) | `(3.5, 3.5)`, `(32.5, 3.5)`, `(3.5, 31.5)`, `(32.5, 31.5)` mm (`Ø6.0 mm` screw-head keepout) | `0.00 mm` (NPTH) |

Run `py -3 scripts/board_space.py` for every part's model height. It moves
each model by its saved scale, rotation and offset first, as KiCad draws it,
and says which models are missing.
