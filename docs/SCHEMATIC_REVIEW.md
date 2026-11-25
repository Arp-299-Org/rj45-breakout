# Schematic review

You are the critic for the schematic that `board/board.json` names under
`schematic`. Read `.agents/critics.md` first: its rules bind you. Copy the
schematic with its `.kicad_pro`, `sym-lib-table` and symbol libraries beside
it.

The owner's standard: before they see the schematic it must be beautiful and
easy to read. ERC zero, a valid netlist and a readable source file do not
meet that standard. Only looking does. Rules:

1. **Look at the rendered sheet as a human electrical reviewer would.** Open
   the export images directly, the whole sheet first at overview
   scale, then every functional block at a scale where pin names and values
   are legible. Describe what you literally see. Judge: are functional blocks
   and signal flow understandable left to right; are references, values, pin
   names and numbers, net labels and notes legible and visibly attached to
   the objects they belong to; are junction dots, crossings, no-connects and
   dangling ends unambiguous; do labels, wires, symbols or fields overlap,
   clip, hide pins or run off the sheet; are power and ground domains,
   connector direction and pin numbering, resets, enables, optional or DNP
   paths visually clear; do global labels turn the design into an
   unexplained connectivity maze. Every one of these is a finding when it
   fails, with the sheet location.

2. **The board must follow the schematic.** Export the netlist from your copy
   and compare components, values, footprints and pin connectivity against
   the board the description names under `pcb`. Every disagreement is a
   finding.

3. **Pin order from both sides.** For every connector, state the pin order as
   the schematic draws it and as the mating part's datasheet numbers it, from
   both mating viewpoints, and confirm the mating part's circuits end to end
   by name.

A finding's location is its place on the sheet. After the findings, give a
short readability verdict in plain words: would a competent stranger
understand this sheet in five minutes, and what stops them.
