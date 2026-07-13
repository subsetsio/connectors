"""Download specs for the World Glacier Monitoring Service connector."""

from __future__ import annotations

from subsets_utils import NodeSpec

from nodes.amce_glacier import fetch_amce_glacier
from nodes.amce_global import fetch_amce_global
from nodes.amce_region import fetch_amce_region
from nodes.fog import fetch_fog_table
from nodes.mb_ref import fetch_mb_ref


DOWNLOAD_SPECS: list[NodeSpec] = [
    NodeSpec(id="wgms-amce-glacier", fn=fetch_amce_glacier, kind="download"),
    NodeSpec(id="wgms-amce-global", fn=fetch_amce_global, kind="download"),
    NodeSpec(id="wgms-amce-region", fn=fetch_amce_region, kind="download"),
    NodeSpec(id="wgms-fog-agency", fn=fetch_fog_table, kind="download"),
    NodeSpec(id="wgms-fog-change", fn=fetch_fog_table, kind="download"),
    NodeSpec(id="wgms-fog-change-band", fn=fetch_fog_table, kind="download"),
    NodeSpec(id="wgms-fog-event", fn=fetch_fog_table, kind="download"),
    NodeSpec(id="wgms-fog-front-variation", fn=fetch_fog_table, kind="download"),
    NodeSpec(id="wgms-fog-glacier", fn=fetch_fog_table, kind="download"),
    NodeSpec(id="wgms-fog-mass-balance", fn=fetch_fog_table, kind="download"),
    NodeSpec(id="wgms-fog-mass-balance-band", fn=fetch_fog_table, kind="download"),
    NodeSpec(id="wgms-fog-mass-balance-point", fn=fetch_fog_table, kind="download"),
    NodeSpec(id="wgms-fog-person", fn=fetch_fog_table, kind="download"),
    NodeSpec(id="wgms-fog-state", fn=fetch_fog_table, kind="download"),
    NodeSpec(id="wgms-fog-state-band", fn=fetch_fog_table, kind="download"),
    NodeSpec(id="wgms-mb-ref", fn=fetch_mb_ref, kind="download"),
]
