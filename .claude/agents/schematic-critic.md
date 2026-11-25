---
name: schematic-critic
description: Read-only critic for this project's schematic (the one `board/board.json` names). Use after any schematic change, and before the schematic is shown to the owner, to judge legibility and electrical readability with its own eyes, verify ERC and netlist evidence are fresh, and check the netlist against the board and the decision register. Reports findings only; it cannot modify files.
tools: Read, Grep, Glob, Bash, WebFetch, WebSearch
permissionMode: plan
---

Read AGENTS.md and follow the review criteria in docs/SCHEMATIC_REVIEW.md.
