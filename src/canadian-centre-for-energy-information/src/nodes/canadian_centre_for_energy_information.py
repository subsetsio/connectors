"""Canadian Centre for Energy Information (CCEI) connector.

Mechanism: SDMX 2.1 REST API (https://energy-information.canada.ca/sdmx/rest/).
One download node per rank-accepted dataflow. Each node fetches the full table
for its dataflow in a single request as SDMX-CSV and saves the raw CSV verbatim.

Shape: stateless full re-pull. The corpus is small (~100 modest dataflows) and
the API exposes no incremental/since filter for whole-flow extraction, so every
refresh re-fetches each flow in full and overwrites — revisions are picked up
for free. (Per research download_handoff.)

Format gotcha: the documented `?format=text/csv` query param is ignored by this
server — it returns generic SDMX-XML. CSV must be requested via the `Accept:
text/csv` header. Each dataflow's CSV has its own dimension columns (DSD), but
all share DATAFLOW, FREQ, TIME_PERIOD, OBS_VALUE and the standard SDMX attribute
columns. Because the dimension columns differ per flow we save raw CSV (stable
within a flow) rather than a fixed parquet schema, and the transform is a generic
pass that casts OBS_VALUE and drops the constant DATAFLOW column.
"""

from subsets_utils import (
    NodeSpec,
    get,
    save_raw_file,
)
from constants import ENTITY_IDS

SLUG = "canadian-centre-for-energy-information"
SDMX_BASE = "https://energy-information.canada.ca/sdmx/rest/data/"

# spec id (lowercased, _ -> -) is lossy, so map it back to the original
# AGENCY:FLOW entity id needed to build the SDMX path.
SPEC_TO_ENTITY = {
    f"{SLUG}-{eid.lower().replace('_', '-')}": eid for eid in ENTITY_IDS
}


def _fetch_csv(url: str) -> bytes:
    resp = get(url, headers={"Accept": "text/csv"}, timeout=(10.0, 300.0))
    resp.raise_for_status()
    return resp.content


def fetch_one(node_id: str) -> None:
    asset = node_id  # the runtime passes the spec id; it IS the asset name
    entity_id = SPEC_TO_ENTITY[node_id]
    agency, flow = entity_id.split(":", 1)
    # No key segment (trailing slash) -> the entire dataflow in one request.
    url = f"{SDMX_BASE}{agency},{flow}/"
    content = _fetch_csv(url)
    save_raw_file(content, asset, extension="csv")


DOWNLOAD_SPECS = [
    NodeSpec(
        id=f"{SLUG}-{eid.lower().replace('_', '-')}",
        fn=fetch_one,
        kind="download",
    )
    for eid in ENTITY_IDS
]
