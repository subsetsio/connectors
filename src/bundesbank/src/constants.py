"""Dataset-id selections for the bundesbank connector.

These lists name which datasets/entities the connector pulls. They are data, not
logic, so they live here instead of being hardcoded in the node module(s), and are
imported back as e.g. ``from constants import ENTITY_IDS``.

This file sits outside ``nodes/`` on purpose: ``load_nodes`` only scans ``nodes/``,
so it is never treated as a node module, and the runner puts ``src/`` on the path
so the import resolves at validation and at runtime.
"""


ENTITY_IDS = [
    "BBAF3", "BBAI3", "BBAPV", "BBASV", "BBBEK1", "BBBEK2", "BBBEK3", "BBBEK4",
    "BBBEK5", "BBBK1", "BBBK10", "BBBK11", "BBBK12", "BBBK2", "BBBK3", "BBBK4",
    "BBBK5", "BBBK6", "BBBK7", "BBBK8", "BBBK9", "BBBP1", "BBBPS", "BBBS2",
    "BBBU2", "BBBZ1", "BBDA1", "BBDB2", "BBDE1", "BBDL1", "BBDP1", "BBDR1",
    "BBDY1", "BBDZ1", "BBEE1", "BBEE5", "BBEX3", "BBFBOPV", "BBFEPOEV",
    "BBFFDIPV", "BBFFDITV", "BBFI1", "BBFI3", "BBGFS1", "BBIB1", "BBIG1",
    "BBIM1", "BBIN1", "BBK10", "BBKRT", "BBMF1", "BBMFK1", "BBMMB", "BBMME",
    "BBMMS", "BBMMU", "BBNZ1", "BBSAP", "BBSDI", "BBSDP", "BBSEI", "BBSF2",
    "BBSF3", "BBSHI", "BBSIS", "BBSSP", "BBSSY", "BBUMF", "BBWCAF1", "BBXE1",
    "BBXF1", "BBXL3", "BBXN1", "BBXP2", "BBXS1", "BBZVS01", "BBZVS02", "BBZVS03",
    "BBZVS04", "BBZVS05", "BBZVS06", "BBZVS08", "BBZVS11", "BBZVS12", "BBZVSSSI",
]
