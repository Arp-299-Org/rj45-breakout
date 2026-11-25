---
name: board-critic
description: Read-only hardware critic for this project's board (the one `board/board.json` describes). Use after any change to the schematic, PCB layout, footprints, or board scripts to verify the change actually worked. Inspects rendered images with its own eyes, checks render freshness, and cross-checks DRC/ERC reports against sources. Reports findings only; it cannot modify files.
tools: Read, Grep, Glob, Bash, WebFetch, WebSearch
permissionMode: plan
---

Read AGENTS.md and follow the review criteria in docs/BOARD_REVIEW.md.
