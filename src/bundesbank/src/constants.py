"""Dataset ids pulled from Bundesbank — data, not logic.

The 85 SDMX dataflow ids the accept step accepted, enumerated by collect from
https://api.statistiken.bundesbank.de/rest/metadata/dataflow/BBK.

BBK10 is deliberately absent: it holds the legacy BBK01 key family, whose last
observation is 2014-Q1, and the accept policy rejects it as stale.
"""

ENTITY_IDS = [
    "BBAF3", "BBAI3", "BBAPV", "BBASV", "BBBEK1", "BBBEK2", "BBBEK3",
    "BBBEK4", "BBBEK5", "BBBK1", "BBBK10", "BBBK11", "BBBK12", "BBBK2",
    "BBBK3", "BBBK4", "BBBK5", "BBBK6", "BBBK7", "BBBK8", "BBBK9", "BBBP1",
    "BBBPS", "BBBS2", "BBBU2", "BBBZ1", "BBDA1", "BBDB2", "BBDE1", "BBDL1",
    "BBDP1", "BBDR1", "BBDY1", "BBDZ1", "BBEE1", "BBEE5", "BBEX3",
    "BBFBOPV", "BBFEPOEV", "BBFFDIPV", "BBFFDITV", "BBFI1", "BBFI3",
    "BBGFS1", "BBIB1", "BBIG1", "BBIM1", "BBIN1", "BBKRT", "BBMF1",
    "BBMFK1", "BBMMB", "BBMME", "BBMMS", "BBMMU", "BBNZ1", "BBSAP", "BBSDI",
    "BBSDP", "BBSEI", "BBSF2", "BBSF3", "BBSHI", "BBSIS", "BBSSP", "BBSSY",
    "BBTHB", "BBUMF", "BBWCAF1", "BBXE1", "BBXF1", "BBXL3", "BBXN1",
    "BBXP2", "BBXS1", "BBZVS01", "BBZVS02", "BBZVS03", "BBZVS04", "BBZVS05",
    "BBZVS06", "BBZVS08", "BBZVS11", "BBZVS12", "BBZVSSSI"
]
