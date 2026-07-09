"""Dataset-id selections for the ecb connector.

These lists name which datasets/entities the connector pulls. They are data, not
logic, so they live here instead of being hardcoded in the node module(s), and are
imported back as e.g. ``from constants import ENTITY_IDS``.

This file sits outside ``nodes/`` on purpose: ``load_nodes`` only scans ``nodes/``,
so it is never treated as a node module, and the runner puts ``src/`` on the path
so the import resolves at validation and at runtime.
"""


ENTITY_IDS = [
    "AGR", "AME", "BKN", "BLS", "BNT", "BOP", "BSI", "BSP", "CAR", "CBD",
    "CBD2", "CCP", "CES", "CISS", "CLIFS", "CPP", "CSEC", "DCM", "DWA", "ECS",
    "EFS", "EMMS", "EON", "ESA", "ESB", "EST", "EWT", "EXR", "FM", "FVC",
    "FXI", "GST", "HICP", "ICB", "ICO", "ICP", "IFI", "ILM", "INW", "IRS",
    "IVF", "KRI", "LIG", "MFI", "MIR", "MMS", "MMSR", "MPD", "NEC", "OFI",
    "OMO", "PAY", "PCN", "PCP", "PCT", "PDD", "PEM", "PFB", "PFBM", "PFBR",
    "PIS", "PLB", "PMC", "PPC", "PSN", "PSS", "PST", "PTN", "PTT", "RA",
    "RAI", "RDE", "RDF", "RESC", "RESH", "RESR", "RESV", "RIR", "RPP", "RPV",
    "RTD", "SAFE", "SEC", "SEE", "SESFOD", "SHI", "SHS", "SHSS", "SPF", "SSI",
    "SSP", "SST", "ST1", "ST3", "STBS", "STP", "STS", "SUP", "SUR", "TGB",
    "TRD", "WTS", "YC",
]
