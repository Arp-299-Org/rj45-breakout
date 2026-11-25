# Board decisions

The owner's decisions for this board and why the board is like this. The
Decisions card writes this file; every other card reads it, and a critic
reports anything under review that contradicts it.

## How a decision goes in

- Only the owner decides product behavior, parts, placement, cost, purchases
  and tradeoffs. A line goes in after the owner adopts it, in the owner's
  words, with the date.
- Write what is true now. When a decision changes, rewrite its line; git
  keeps the old one.
- Each decision says why, so a later agent can tell when it no longer holds.
- Numbers name their source: a datasheet page, a measurement (who, when, with
  what), or "local choice" with whose.
- A question still open is an open issue in `tools/board_graph.json`, with the
  card it must close before. It is not a decision.

## Why it is like this

One bullet per decision, the subject in bold: what was decided, why, the
owner's words and the date.

- **Product scope:** Simple passive RJ45 (8P8C) to 2.54 mm header breakout board with no magnetics or LEDs, inspired by Caleb (@OSHBuilt) wanting a clean AI-designed RJ45 breakout workflow. Owner words: "This project exists because i saw this tweet" / "all your recs", 2026-11-25.
- **RJ45 jack style:** Right-angle, unshielded 8P8C SMT jack with mechanical retention (plastic locating pegs and/or SMT anchor tabs, never signal-pads-only) sourced from LCSC in-stock SMT inventory. Unshielded avoids a 9th shield pin; SMT fits JLCPCB Economic PCBA without through-hole hand-solder surcharges; mechanical retention protects pads against cable pull. Owner words: "all your recs", 2026-11-25.
- **Breakout header:** Single-row 1x8, 2.54 mm pitch (standard header pitch) SMT vertical male pin header, factory-placed for a turnkey zero-soldering board, with no shield pin. Single-row 1x8 fits solderless breadboards and leaves clean room for pin labels next to each pin. Owner words: "all your recs, smt factory place vertical male for turnkey", 2026-11-25.
- **Fabrication and assembly target:** JLCPCB 2-layer FR-4 with JLCPCB Economic SMT assembly for fast turnaround and full end-to-end PCBA flow. Owner words: "all your recs, smt factory place vertical male for turnkey", 2026-11-25.
- **Mounting holes:** 4x M3 corner mounting holes (3.2 mm NPTH drill, ~6.0 mm screw-head clearance keepout; owner local choice) to match standard M3 standoffs, accepting a slightly larger outline to preserve clean clearances. Owner words: "and i think 4x M3 for a slightly larger board", 2026-11-25.
- **Target board size and silkscreen:** Compact outline sized around the RJ45 jack, 1x8 header, and 4x M3 corner holes (target approximately 32x35 mm, owner local choice; final dimensions settled at Placement), with pin numbers `1` through `8` and T568B wire color labels (`W/O`, `O`, `W/G`, `B`, `W/B`, `G`, `W/Br`, `Br`) on silkscreen (top and bottom where space permits). Owner words: "yes that sounds good" / "and i think 4x M3 for a slightly larger board", 2026-11-25.

## Parts on hand

What the owner already has for these boards (modules, displays, cables), with
quantities. The Order card lists what to buy against this.

## Orientation preview

Gate G11 of `board/ORDER_PACKAGE_CONTRACT.md`: for each order, the date and
the owner's result of looking at the assembler's placement preview for every
polarized or orientation-sensitive part.

## Waivers

Each accepted exception to a check: the check, the item, why, the owner's
words and the date. The waiver file the board description names holds the
same exceptions as data for the scripts.
