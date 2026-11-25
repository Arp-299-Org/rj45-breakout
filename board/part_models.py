"""Parametric STEP 3D models built from datasheet dimensions for rj45-breakout."""
from __future__ import annotations

import importlib.util
import os
import pathlib
import sys


def _add_board_graph_scripts() -> None:
    """Make board-graph's kicad_step_model helper importable via env var or installed package."""
    candidates: list[pathlib.Path] = []
    env_root = os.environ.get("BOARD_GRAPH_TOOL_ROOT")
    if env_root:
        candidates.append(pathlib.Path(env_root) / "scripts")
    spec = importlib.util.find_spec("board_graph_entry")
    if spec and spec.origin:
        base = pathlib.Path(spec.origin).resolve().parent
        candidates.extend((base / "scripts", base / "_board_graph_data" / "scripts"))
    for path in candidates:
        if (path / "kicad_step_model.py").is_file() and str(path) not in sys.path:
            sys.path.insert(0, str(path))
            return


_add_board_graph_scripts()
from kicad_step_model import BLACK, TIN, box, cylinder  # noqa: E402

GOLD = (0.85, 0.70, 0.25)


def heling_rj45():
    """Heling MJ56881-B011-HLRN1-C (C501473) right-angle unshielded 8P8C SMT jack.

    Datasheet page 1: 15.20 mm wide (X), 12.95 mm deep (Y, port opening at +Y),
    12.50 mm high above PCB mount face (Z), 2x 1.00 mm locating pegs at y=-3.975,
    2x SMT metal anchor tabs at x=+-6.32, y=+0.925, and 8 gull-wing leads at y=[-7.875, -6.475].
    """
    prisms = [
        # Rear body block and side/top housing walls leaving front (+Y) port cavity visible
        box(-7.60, -6.475, 0.20, 7.60, 0.50, 12.50, BLACK),
        box(-7.60, 0.50, 0.20, -6.00, 6.475, 12.50, BLACK),
        box(6.00, 0.50, 0.20, 7.60, 6.475, 12.50, BLACK),
        box(-6.00, 0.50, 0.20, 6.00, 6.475, 1.40, BLACK),
        box(-6.00, 0.50, 10.60, 6.00, 6.475, 12.50, BLACK),
        # Latch slot roof inset cheeks
        box(-6.00, 0.50, 8.20, -2.40, 6.475, 10.60, BLACK),
        box(2.40, 0.50, 8.20, 6.00, 6.475, 10.60, BLACK),
        # Two metal SMT anchor tabs
        box(-7.50, -1.50, 0.00, -4.95, 3.35, 0.30, TIN),
        box(4.95, -1.50, 0.00, 7.50, 3.35, 0.30, TIN),
        # Two plastic locating pegs (datasheet: dia 1.00 mm, at x=+-5.60, y=-3.975)
        cylinder(-5.60, -3.975, 0.50, -0.80, 0.20, BLACK),
        cylinder(5.60, -3.975, 0.50, -0.80, 0.20, BLACK),
    ]
    # 8 gull-wing contacts exiting -Y face (pin 1 at +3.57, pin 8 at -3.57)
    for i in range(8):
        cx = 3.57 - i * 1.02
        prisms.append(box(cx - 0.15, -7.875, 0.00, cx + 0.15, -6.475, 0.45, GOLD))
        prisms.append(box(cx - 0.15, 1.50, 1.40, cx + 0.15, 5.50, 1.90, GOLD))
    return prisms


def hanxia_1x8_header():
    """hanxia HX PZ2.54-1x8P TP-ZQ (C42453975) 2.54 mm 1x8 Type B staggered SMT vertical male header.

    Datasheet page 1: body 20.12 x 2.50 mm, insulator top 3.20 mm, pin 6.00 mm above insulator
    (total height 9.20 mm), 0.64 mm square pins, staggered SMT feet (pin 1 south +Y, pin 2 north -Y).
    """
    prisms = [
        box(-10.06, -1.25, 0.70, 10.06, 1.25, 3.20, BLACK),
    ]
    for i in range(8):
        cx = -8.89 + i * 2.54
        # Vertical 0.64 mm square pin up to 9.20 mm
        prisms.append(box(cx - 0.32, -0.32, 0.70, cx + 0.32, 0.32, 9.20, GOLD))
        # Staggered SMD foot: odd pins (i even: 1,3,5,7) face +Y south; even pins face -Y north
        if i % 2 == 0:
            prisms.append(box(cx - 0.32, -0.32, 0.00, cx + 0.32, 2.50, 0.70, GOLD))
        else:
            prisms.append(box(cx - 0.32, -2.50, 0.00, cx + 0.32, 0.32, 0.70, GOLD))
    return prisms


PARTS = {
    "Heling_MJ56881-B011-HLRN1-C": heling_rj45,
    "Hanxia_HX_PZ2.54-1x8P_TP-ZQ": hanxia_1x8_header,
}
