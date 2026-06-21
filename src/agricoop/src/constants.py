"""Entity union for agricoop — the rank-accepted collect entities and the
data.gov.in resource id (index_name) each one publishes from.

Copied from data/sources/agricoop/work/entity_union.json. Each collect entity is
one tabular resource on the data.gov.in OGD platform, fetched via
https://api.data.gov.in/resource/{resource_id}.

Why only these 5 of the 21 collect entities are built (the rest scored below the
publish threshold for concrete, verified reasons):
  - `agmarknet` / `kcc` corpora: their per-slice resources return total=0 via the
    resource API (external-webservice proxies — catalog husks, no served rows).
  - `crop-wise-irrigated-area-LUS` / `total-crop-area-LUS`: resource returns
    status=error, total=0 (dead resources).
  - `variety-wise-daily-market-prices` (80.1M rows) and `pm-kisan-beneficiaries`
    (13.0M rows): firehose-scale with NO incremental/since filter on the resource
    endpoint, so a full re-pull every run is infeasible — deferred until an
    incremental path exists.

The 5 built here are bounded, served, and feasible (36 .. 246k rows each).
"""

# collect entity id -> data.gov.in resource index_name
RESOURCE_ID = {
    "classified-area-under-land-use-statistics-lus-3db3addf": "8a3761be-1b0b-423d-a907-1f99870b365a",
    "current-daily-price-of-various-commodities-from-various-mark-1abe392e": "9ef84268-d588-465a-a308-a864a43d0070",
    "district-wise-season-wise-crop-production-statistics-from-19-c33a2e6b": "35be999b-0208-4354-b557-f6ca9a5355de",
    "source-wise-irrigated-area-under-land-use-statistics-lus-3c17d7f6": "512a034f-6924-42d8-9a76-d40bfb56424a",
    "state-wise-number-and-area-of-operational-holdings-for-sched-2273cec3": "0a42f538-0ccc-483f-9a4e-17aa9d146b04",
}

ENTITY_IDS = list(RESOURCE_ID)
