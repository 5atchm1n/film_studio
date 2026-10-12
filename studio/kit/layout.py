"""Layout: named anchors of the standard stage (16:9, Manim units, frame 14.2 × 8).

    ┌ chapter label ─────────────────────────────────────── title / code ┐
    │  CHAT (user)  ──IN_X──▶  CHIP (AI)  ──────▶  PANEL (mechanism)     │   main row  y = OUT_Y
    │                            │ BUS_Y                                 │
    │  ═══════════════ BAND (semantic layer / MCP)  y = BAND_Y ═════════ │
    │  ─────────────── DATA  y = DATA_Y ──────────────────────────────── │
    └────────────────────────────────────────────────────────────────────┘
Answers appear in the chat; the side panel explains the mechanism.
"""

import numpy as np
from manim import LEFT

OUT_Y = 1.15                                  # main row: chat → chip → panel
CHIP_POS = np.array([-1.2, 1.15, 0])          # the AI chip
USER_POS = np.array([-6.55, OUT_Y, 0])        # a user pictogram, before it becomes the chat
CHAT_C = np.array([-4.95, OUT_Y, 0])          # the chat window (the user), left of the chip
CHAT_W, CHAT_H = 3.4, 1.9
IN_X = CHAT_C[0] + CHAT_W / 2                 # right edge of the chat: where questions leave
ANS_POS = np.array([5.55, OUT_Y, 0])          # right-hand side: answers / panels
ANS_IN = ANS_POS + LEFT * 1.25                # left edge of the right-hand panel
BUS_Y = -1.3                                  # where calls leave the chip towards the band
BAND_Y = -2.05                                # the semantic layer band
DATA_Y = -3.35                                # the data row
