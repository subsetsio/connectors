"""Dataset-id selections for the ecb connector.

These lists name which datasets/entities the connector pulls. They are data, not
logic, so they live here instead of being hardcoded in the node module(s), and are
imported back as e.g. ``from constants import ENTITY_IDS``.

This file sits outside ``nodes/`` on purpose: ``load_nodes`` only scans ``nodes/``,
so it is never treated as a node module, and the runner puts ``src/`` on the path
so the import resolves at validation and at runtime.
"""


ENTITY_IDS = [
    "AGR", "AME", "BKN", "BLS", "BNT", "BSI", "BSP", "CAR", "CBD2", "CCP",
    "CES", "CISS", "CLIFS", "CSEC", "DWA", "ECS", "EFS", "EMMS", "EST", "EWT",
    "EXR", "FM", "FVC", "FXI", "HICP", "ICB", "ICO", "ICP", "ILM", "INW",
    "IRS", "IVF", "LIG", "MFI", "MIR", "MMSR", "MPD", "NEC", "OMO", "PAY",
    "PCN", "PCP", "PCT", "PDD", "PEM", "PFBM", "PFBR", "PIS", "PLB", "PMC",
    "PPC", "PSN", "PST", "PTN", "PTT", "RAI", "RDF", "RESC", "RESH", "RESR",
    "RESV", "RTD", "SAFE", "SESFOD", "SHSS", "SPF", "SSI", "SSP", "SST", "STBS",
    "STP", "STS", "SUP", "SUR", "TGB", "TRD", "WTS", "YC",
]
