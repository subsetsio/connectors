"""Dataset-id selections for the central-bank-of-russia connector.

These lists name which datasets/entities the connector pulls. They are data, not
logic, so they live here instead of being hardcoded in the node module(s), and are
imported back as e.g. ``from constants import ENTITY_IDS``.

This file sits outside ``nodes/`` on purpose: ``load_nodes`` only scans ``nodes/``,
so it is never treated as a node module, and the runner puts ``src/`` on the path
so the import resolves at validation and at runtime.
"""


ENTITY_IDS = [
    "pub-10-ds-17", "pub-10-ds-18", "pub-11-ds-19", "pub-11-ds-20",
    "pub-11-ds-21", "pub-11-ds-22", "pub-11-ds-23", "pub-14-ds-25",
    "pub-14-ds-26", "pub-14-ds-27", "pub-14-ds-28", "pub-14-ds-29",
    "pub-15-ds-30", "pub-15-ds-31", "pub-15-ds-32", "pub-15-ds-33",
    "pub-15-ds-34", "pub-16-ds-35", "pub-16-ds-36", "pub-18-ds-37",
    "pub-18-ds-38", "pub-19-ds-39", "pub-19-ds-40", "pub-20-ds-41",
    "pub-20-ds-42", "pub-20-ds-43", "pub-21-ds-44", "pub-21-ds-45",
    "pub-21-ds-46", "pub-21-ds-47", "pub-21-ds-48", "pub-21-ds-55",
    "pub-21-ds-56", "pub-22-ds-49", "pub-22-ds-50", "pub-22-ds-51",
    "pub-23-ds-52", "pub-23-ds-53", "pub-23-ds-54", "pub-25-ds-140",
    "pub-25-ds-58", "pub-25-ds-59", "pub-25-ds-60", "pub-25-ds-61",
    "pub-25-ds-62", "pub-25-ds-63", "pub-25-ds-64", "pub-25-ds-65",
    "pub-25-ds-66", "pub-25-ds-67", "pub-25-ds-68", "pub-25-ds-69",
    "pub-25-ds-70", "pub-25-ds-71", "pub-25-ds-72", "pub-25-ds-73",
    "pub-25-ds-74", "pub-25-ds-75", "pub-25-ds-76", "pub-25-ds-77",
    "pub-25-ds-78", "pub-25-ds-79", "pub-28-ds-101", "pub-28-ds-104",
    "pub-28-ds-107", "pub-28-ds-110", "pub-28-ds-113", "pub-28-ds-116",
    "pub-28-ds-119", "pub-28-ds-80", "pub-28-ds-83", "pub-28-ds-86",
    "pub-28-ds-89", "pub-28-ds-92", "pub-28-ds-95", "pub-28-ds-98",
    "pub-29-ds-102", "pub-29-ds-105", "pub-29-ds-108", "pub-29-ds-111",
    "pub-29-ds-114", "pub-29-ds-117", "pub-29-ds-120", "pub-29-ds-81",
    "pub-29-ds-84", "pub-29-ds-87", "pub-29-ds-90", "pub-29-ds-93",
    "pub-29-ds-96", "pub-29-ds-99", "pub-30-ds-100", "pub-30-ds-103",
    "pub-30-ds-106", "pub-30-ds-109", "pub-30-ds-112", "pub-30-ds-115",
    "pub-30-ds-118", "pub-30-ds-121", "pub-30-ds-82", "pub-30-ds-85",
    "pub-30-ds-88", "pub-30-ds-91", "pub-30-ds-94", "pub-30-ds-97",
    "pub-33-ds-127", "pub-33-ds-128", "pub-33-ds-139", "pub-34-ds-129",
    "pub-34-ds-130", "pub-34-ds-131", "pub-34-ds-132", "pub-35-ds-133",
    "pub-35-ds-134", "pub-35-ds-141", "pub-36-ds-135", "pub-36-ds-136",
    "pub-36-ds-137", "pub-36-ds-138", "pub-5-ds-5", "pub-5-ds-6",
    "pub-5-ds-7", "pub-5-ds-8", "pub-8-ds-10", "pub-8-ds-11",
    "pub-8-ds-12", "pub-8-ds-9", "pub-9-ds-13", "pub-9-ds-14",
    "pub-9-ds-15", "pub-9-ds-16",
]
