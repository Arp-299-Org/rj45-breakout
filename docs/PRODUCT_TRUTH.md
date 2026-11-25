# Product truth

What the product is for and what it must do. Every card reads this first. When
another doc disagrees with this one, start here and check against the design.
The owner writes it, or adopts each line before it goes in.

## Mission

Provide a compact, cleanly labeled RJ45-to-header breakout PCB so engineers and makers can probe, patch, or breadboard 8-pin Ethernet/serial/custom RJ45 lines reliably on a workbench.

## What it is

A simple passive breakout board:
- **RJ45 port:** A right-angle, unshielded 8P8C SMT modular jack with mechanical retention (locating pegs and/or anchor tabs) bringing pins `1` to `8` onto the board.
- **Breakout header:** A factory-placed 1x8 single-row 2.54 mm pitch SMT vertical male pin header breaking out pins `1` to `8`.
- **Mounting and form factor:** Compact 2-layer JLCPCB Economic PCBA board (approximately 32x35 mm) with 4x M3 corner mounting holes and clear silkscreen labels for pins `1` to `8` plus T568B wire colors.

## What must be measured

- Point-to-point continuity from every RJ45 contact (pins `1` to `8`) to its corresponding breakout header pin, and isolation between adjacent pins.

## What must not change

- Standard 2.54 mm header spacing so it fits breadboards, jumper wires, or test probes cleanly, with clear pin-number silkscreen labels on both sides where practical.

## Current state

- **Adopted (2026-11-25):** Owner confirmed turnkey JLCPCB Economic SMT assembly with right-angle unshielded 8P8C SMT jack (mechanically retained), 1x8 2.54 mm SMT vertical male header, 4x M3 corner mounting holes, and pin 1 to 8 plus T568B color silkscreen. Next card: Constraints.
