"""Dataset-id selections for the fao connector.

These lists name which datasets/entities the connector pulls. They are data, not
logic, so they live here instead of being hardcoded in the node module(s), and are
imported back as e.g. ``from constants import ENTITY_IDS``.

This file sits outside ``nodes/`` on purpose: ``load_nodes`` only scans ``nodes/``,
so it is never treated as a node module, and the runner puts ``src/`` on the path
so the import resolves at validation and at runtime.
"""


ENTITY_IDS = [
    "AE", "AF", "BE", "CAHD", "CB", "CBH", "CP", "CS", "EA", "EI", "EK", "EM",
    "EMN", "ESB", "ET", "FBS", "FBSH", "FDI", "FDIQ", "FO", "FOP", "FS", "GCE",
    "GF", "GFDI", "GI", "GLE", "GN", "GPP", "GT", "GV", "HCES", "IC", "IG", "LC",
    "MDDW", "MK", "OA", "OEA", "OER", "PD", "PE", "PP", "QCL", "QI", "QV", "RFB",
    "RFM", "RFN", "RL", "RLIS", "RP", "RT", "SCL", "SDGB", "SUA", "SXS", "TCL",
    "TCLI", "TI", "TM", "WCAD",
]
