"""Dataset-id selections for the mpa-singapore connector.

These lists name which datasets/entities the connector pulls. They are data, not
logic, so they live here instead of being hardcoded in the node module(s), and are
imported back as e.g. ``from constants import ENTITY_IDS``.

This file sits outside ``nodes/`` on purpose: ``load_nodes`` only scans ``nodes/``,
so it is never treated as a node module, and the runner puts ``src/`` on the path
so the import resolves at validation and at runtime.
"""


ENTITY_IDS = [
    "d_042dd8b935eab998f389adaf559c80de",
    "d_085682b824700b4e88d946529f503da0",
    "d_0a76d48f3754aafd08f98629324a54c6",
    "d_0c586210d33756a56ef6213078e749aa",
    "d_1714a141d8bbf1996965eb3f71565525",
    "d_48cb38d12697d3463c8cadfb22e6c61d",
    "d_4f5abbf4486bf8e52bbed3be56dde562",
    "d_56f64b2d5a31eb0ee465cc51e83ac60a",
    "d_60410de1bc1e63ddcf51a619081b11b3",
    "d_835d43b9238c6fc877dfcd62d73054a9",
    "d_8392e9bea6ca351a38f67172ccdf6a6a",
    "d_89d2874dad74a273270369334f1e7d28",
    "d_8ab8d71a6bf44097889dd6a3b4258928",
    "d_8f264219109e61fffa87ac64dd5a9a65",
    "d_9adb5ace517591edd9a8c88291ac1f1c",
    "d_a30479ad55e045bcaffacf587d05966c",
    "d_b0c64c019b252698a9f1a222dcf9e0a6",
    "d_c9dcfd8b85990669d1e74dd7ad71eb8b",
    "d_ccb330e6679674ffaa330dc76136e198",
    "d_d48c5a038904f6da3c603cd854b6c191",
    "d_da030f7028200d19ffcbe4a2d71af39c",
    "d_eb1c7c0c9ee013f9be42cc8abf523326",
]
