"""Catalog data for the CAISO OASIS connector (data, not logic).

ENTITY_IDS is the entity union (the rank-accepted collect entities).
REPORTS maps each entity id to the OASIS SingleZip query parameters that were
verified live against https://oasis.caiso.com/oasisapi/SingleZip on 2026-06-22.

Each report is a distinct OASIS `queryname` with its own CSV schema and its own
`version` integer. `market_run_id` selects the market the report is published for
(it is also a column in the CSV). The four LMP reports are fetched for a curated
set of canonical trading-hub pricing nodes (the standard market price references)
rather than ALL_APNODES — that keeps the per-window payload tractable while
publishing the price series consumers actually use. The aggregate/system reports
carry no node filter.
"""

# Canonical CAISO trading hubs — the standard locational price references.
HUB_NODES = "TH_NP15_GEN-APND,TH_SP15_GEN-APND,TH_ZP26_GEN-APND"

# Earliest trade date we backfill from. Current report schema versions (e.g.
# PRC_LMP v12) are stable from well before this; 2019 gives a deep, uniformly
# typed history without reaching into superseded schema versions.
SOURCE_MIN_DATE = "20190101"

REPORTS = {
    "PRC_LMP": {
        "queryname": "PRC_LMP",
        "version": 12,
        "market_run_id": "DAM",
        "node": HUB_NODES,
        "extra": {},
    },
    "PRC_INTVL_LMP": {
        "queryname": "PRC_INTVL_LMP",
        "version": 3,
        "market_run_id": "RTM",
        "node": HUB_NODES,
        "extra": {},
    },
    "PRC_RTPD_LMP": {
        "queryname": "PRC_RTPD_LMP",
        "version": 3,
        "market_run_id": "RTPD",
        "node": HUB_NODES,
        "extra": {},
    },
    "PRC_HASP_LMP": {
        "queryname": "PRC_HASP_LMP",
        "version": 3,
        "market_run_id": "HASP",
        "node": HUB_NODES,
        "extra": {},
    },
    "SLD_FCST": {
        "queryname": "SLD_FCST",
        "version": 1,
        "market_run_id": "DAM",
        "node": None,
        "extra": {},
    },
    "SLD_REN_FCST": {
        "queryname": "SLD_REN_FCST",
        "version": 1,
        "market_run_id": "DAM",
        "node": None,
        "extra": {},
    },
    "ENE_SLRS": {
        "queryname": "ENE_SLRS",
        "version": 1,
        "market_run_id": "DAM",
        "node": None,
        "extra": {},
    },
    "AS_RESULTS": {
        "queryname": "AS_RESULTS",
        "version": 1,
        "market_run_id": "DAM",
        "node": None,
        "extra": {"anc_type": "ALL", "anc_region": "ALL"},
    },
    "AS_REQ": {
        "queryname": "AS_REQ",
        "version": 1,
        "market_run_id": "DAM",
        "node": None,
        "extra": {"anc_type": "ALL", "anc_region": "ALL"},
    },
    "PRC_FUEL": {
        "queryname": "PRC_FUEL",
        "version": 1,
        "market_run_id": None,
        "node": None,
        "extra": {"fuel_region_id": "ALL"},
    },
}

ENTITY_IDS = list(REPORTS.keys())
