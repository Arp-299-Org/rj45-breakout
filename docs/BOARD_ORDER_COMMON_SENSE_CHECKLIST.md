# PCB order common-sense checklist

This checklist is a release gate before money is spent on any PCB or assembly
order. A clean DRC and ERC are necessary, but not enough. The board must also
be physically buildable, solderable, testable, and usable with the ordinary
tools and workflow the builder actually has.

Every applicable item must be marked **PASS** with direct evidence.
**UNKNOWN**, **ASSUMED** or **NOT CHECKED** means **DO NOT ORDER**.

This applies to the evidence available before ordering: the design, drawings,
manufacturing outputs and quote. Items the owner explicitly deferred until
after the order (an enclosure, a fixture, a physical dry fit, first-article
tests) stay delivery, assembly and test cards. A completed pre-order checklist
is not a claim that the physical first article passed.

## What went wrong before

This section exists so a past failure is checked for by name on every later
order. Write each one plainly: what happened, how it was found, and which row
below now catches it.

- (none recorded yet)

## Before ordering

Real physical questions must not be answered with narrower checks reported as
proof. A clean DRC does not prove a land can be soldered, a matching net name
does not prove a mating order, and a 3D render does not prove a part fits.
Nothing on an earlier revision is evidence that a joint or hole on this one is
right.

No package is ready until:

- the owner has approved placement on a rendered view;
- schematic, board, firmware (where there is firmware) and connector mappings
  agree;
- gates G1 to G12 of `board/ORDER_PACKAGE_CONTRACT.md` pass on the exact files;
- this checklist passes;
- the owner has looked at the assembler's placement preview for every
  polarized or orientation-sensitive part.

## 1. The board can actually be assembled

These rows are not left for the order. The Footprints card runs
`scripts/board_manual_joints.py` on every joint soldered by hand, and CI runs
it with the pad mask and thermal relief checks on every board change. Read
`board/reports/footprints/manual_joints.md` for the rows below, then check the
final files again here.

- [ ] Every manually soldered pin has a real exposed copper land in the final
      top and bottom solder-mask Gerbers.
- [ ] Every plated hole fits the real production pin, including square-pin
      diagonal, plating tolerance, and practical insertion clearance.
- [ ] Standard, readily available pin headers and connectors were evaluated
      before specifying proprietary, unusually small, low-profile, or expensive
      hardware. Any nonstandard choice has a demonstrated requirement that a
      standard part cannot meet.
- [ ] Header-hole sizing accepts the intended ordinary production header, not
      merely the one specialty sample used during CAD work.
- [ ] Every hand-soldered pad has enough exposed annular ring for an ordinary
      soldering-iron tip to contact the pin and pad together.
- [ ] Ground and power pads have thermal relief or a documented, tested
      soldering method using the builder's normal equipment.
- [ ] No required joint becomes inaccessible after another part is installed.
- [ ] The assembly order is written down and can be completed without rework,
      bodge wires, destructive clipping, or specialty equipment unless the
      builder explicitly accepted that step before ordering.
- [ ] Every connector, module, switch, potentiometer, encoder, jack, and display
      has been checked against the manufacturer's drawing or a measured physical
      sample, not only a library footprint or 3D model.
- [ ] Every connector's mating order has been checked from both sides as the
      parts are assembled: pin 1 on the board and pin 1 on the mating part.
- [ ] Every part can be identified from the board: references or labels on the
      silkscreen, readable beside their parts.

## 2. The factory/manual boundary is unambiguous

- [ ] A reference-by-reference list states what the PCB assembler installs and
      what the builder installs.
- [ ] Every factory-installed part appears in the final BOM and placement file.
- [ ] Every intentionally manual or omitted part is clearly labeled and has a
      practical installation procedure.
- [ ] No part is assumed to arrive loose unless the supplier explicitly confirms
      that it will be supplied loose.
- [ ] Both assembly sides, special processes, and additional charges match the
      quote and the final review screen.

## 3. The final manufacturing files say what the design intends

- [ ] The exact ZIP being uploaded (not merely the editable board) has been
      inspected for copper, solder mask, paste, silkscreen, drills, slots, and
      board outline.
- [ ] Every through-hole component has the expected holes and solder-mask
      openings on both sides.
- [ ] Every surface-mount component has the expected copper, mask, and paste
      apertures on its assembly side, with no unintended paste on the other side.
- [ ] Plated and non-plated holes are correctly classified.
- [ ] Slots, cutouts, castellations, and edge features appear in the fabricator's
      viewer exactly as intended.
- [ ] Copper-to-edge, hole-to-edge, and solder-mask clearances meet the actual
      fabricator's capabilities.
- [ ] Layer count, order, thickness, copper weight, finish, color, and stackup in
      the quote match the intended board.
- [ ] The BOM and placement files match the exact Gerber revision and use the
      same coordinate origin.

### Fabricator limits KiCad does not check

Name the fabricator and the stackup selected on the quote. Fill the table from
the fabricator's published capabilities page, with the date it was read, and
re-check it before every order: fabricator limits change without notice.

| Limit | Value | Read on |
|---|---|---|
| Non-plated internal slot, minimum width | | |
| Non-plated slot tolerance | | |
| Copper to routed edge or slot | | |
| Routed feature tolerance | | |
| Plated slot, minimum width | | |
| Plated hole finished size tolerance | | |

KiCad DRC checks copper-to-edge and copper-to-cutout clearance at the
project's own rule. It does not check milled slot width, inside corner radius,
or any other fabricator process limit. Those are checked by hand against this
table, and the stackup selection on the quote is checked against the one named
here.

## 4. The finished board fits and can be used

- [ ] Board dimensions and mounting-hole locations have been measured against
      the enclosure or a dimensioned mechanical drawing.
- [ ] Component bodies, solder joints, pins, cables, nuts, standoffs, keycaps,
      displays, and connectors clear one another in all three dimensions.
- [ ] Display height, button and key height, knob height, and connector depth
      are established by real dimensions and an explicit tolerance stack.
- [ ] Where standoffs or bosses establish module height, the connector is not
      also being used as an unnecessary precision spacer. The fastener stack
      controls height and the pins only make the electrical connection.
- [ ] USB, card, audio, power, reset and boot, and other required openings
      remain reachable after final assembly.
- [ ] A module that can only be recovered through its own port (a bootloader
      over USB, a programming header) keeps that port reachable.
- [ ] No part blocks access to another part that may need rework or service.
- [ ] No normal assembly or enclosure fastener presses on copper, solder joints,
      components, or fragile module areas.
- [ ] Tooling rails, tabs, V-scores, and panelization are identified from the
      actual production review; who removes them and how is written down.
- [ ] Any required rail or tab removal can be done safely with tools the builder
      already owns, unless another method was explicitly approved before order.

## 5. The board can be powered and tested safely

- [ ] Power-source voltage, polarity, grounding, protection, and expected current
      are documented and checked at every connector and module boundary.
- [ ] There is a staged first-power procedure with current limiting and expected
      resistance and voltage measurements before expensive modules are installed.
- [ ] Critical rails, ground, reset and boot, communications, outputs, inputs,
      and storage have reachable test points or accessible component pins.
- [ ] The board can be tested far enough to distinguish a PCB fault from a module,
      firmware, cable, or assembly fault.
- [ ] No test requires sacrificing a board or risking every expensive module at
      once.

## 6. Parts and costs are real

- [ ] Every builder-supplied item has an exact manufacturer part number, quantity
      per board, working vendor link, current stock status, and current unit cost.
- [ ] Already-owned and already-ordered quantities are separated from quantities
      still needed.
- [ ] Necessary consumables and ordinary assembly hardware are included; optional
      tools and upgrades are not disguised as required parts.
- [ ] Expensive or unusual components have a documented reason and a checked
      lower-cost alternative.
- [ ] The per-board material cost uses one stable definition and does not silently
      add labor, testing, billing, overhead, or other categories.
- [ ] Quantity pricing, shipping, assembly fees, setup fees, and attrition are
      shown separately rather than buried in the component cost.

## 7. Independent release sanity check

- [ ] A pin-by-pin and manual-joint table has been generated from the final files
      and reviewed for hole size, mask opening, exposed land, and accessibility.
- [ ] A reference-by-reference assembly table has been compared with the physical
      build sequence.
- [ ] Automated checks explicitly cover through-hole solder-mask openings; a
      surface-mount-only mask check is not accepted as evidence.
- [ ] Every exception is written in plain language with its consequence and has
      been explicitly accepted by the builder.
- [ ] The final order preview has been reviewed without relying on a previous
      report, stale screenshot, or an assistant's unsupported assurance.
- [ ] The person spending the money receives a short final summary containing:
      exact files, exact revision, quantity, cost, factory-installed parts,
      manual work, known exceptions, and remaining risks.

## Release rule

The board is **READY TO ORDER** only when every applicable box above is a proven
PASS. If a claim cannot be demonstrated from the final manufacturing files,
manufacturer data, a measured physical part, or a tested assembly, the claim is
not proven and the order remains on hold.
