"""National Bank of Belgium (NBB.Stat) connector.

Mechanism: SDMX 2.1 REST dissemination API at
https://nsidisseminate-stat.nbb.be/rest (the backing API of the NBB.Stat Data
Explorer). One publishable subset per dataflow: each dataflow is a
self-contained statistical cube with its own data-structure definition.

Fetch shape: **stateless full re-pull**. Each refresh re-downloads every
dataflow's whole cube as SDMX-CSV (one request per flow, key='all'). SDMX has
no usable incremental delta for our whole-table snapshot pattern.

Raw format: we stream the SDMX-CSV response and re-emit it row-by-row as gzipped
NDJSON with **verbatim string values**. This is deliberate: the cubes are
heterogeneous (each flow has its own dimension columns) and TIME_PERIOD mixes
annual ("2015"), quarterly ("2015-Q1") and monthly ("2015-02") forms within and
across flows — DuckDB's CSV auto-sniffer would type TIME_PERIOD as BIGINT off an
all-integer sample and then fail on the first "2015-02". Writing every value as a
JSON string forces the downstream auto-reader to VARCHAR, and the transform casts
only OBS_VALUE. The row-at-a-time stream keeps memory bounded for the large cubes.

SDMX-CSV always carries DATAFLOW, TIME_PERIOD and OBS_VALUE columns; the
transform keeps every dimension/attribute column and casts OBS_VALUE to DOUBLE.
"""

import csv
import json

import httpx

from subsets_utils import (
    NodeSpec,
    get_client,
    raw_writer,
    transient_retry,
)

SLUG = "national-bank-of-belgium"
BASE = "https://nsidisseminate-stat.nbb.be/rest"
# SDMX-CSV 1.0 — flat table with a DATAFLOW column, one column per dimension /
# attribute, plus TIME_PERIOD and OBS_VALUE. ASCII-only header.
CSV_ACCEPT = "application/vnd.sdmx.data+csv;version=1.0.0"
RAW_EXT = "ndjson.gz"

# The rank-accepted entity union — copied verbatim from
# data/sources/national-bank-of-belgium/work/entity_union.json (163 dataflows).
# Excluded by rank: (1) the five 1GB+ national/community-concept foreign-trade
# firehoses (DF_EXTTRADE{BENAT,BECOM,BXNAT,VLNAT,WLNAT}) — too large to build
# reliably, covered by their _Overview / TEC variants; (2) the four STEC flows
# (DF_STEC01/02/03, DF_STEC_COMPLETE) which carry no data mapping (404 on fetch);
# (3) seven dataflows that the API returns byte-identical to a sibling over the
# same cube (DF_FAHHNFC_S14, DF_FDI_IO, DF_FINACC2010_WEALTH, DF_FINGOV_BALANCE,
# DF_NADETP4_DISS, DF_NASECDET2010_S14_DISS, DF_NFGOV_NET_DISS) — sibling kept.
from constants import ENTITY_IDS


def _spec_id(entity_id: str) -> str:
    return f"{SLUG}-{entity_id.lower().replace('_', '-')}"


# spec id -> the original (case-sensitive) SDMX dataflow id. Built from the
# literal above; reversing the slug transform is lossy (some ids carry mixed
# case, e.g. DF_EXTTRADEBECOM_Overview), so we keep an explicit map.
SPEC_TO_FLOW = {_spec_id(e): e for e in ENTITY_IDS}


@transient_retry()
def _download_cube(flow: str, asset: str) -> None:
    """Stream one dataflow's SDMX-CSV cube and re-emit it as gzipped NDJSON.

    Streamed and parsed row-by-row (never buffering the whole body), so memory
    stays bounded. Values are written verbatim as JSON strings; the transform
    handles typing. A retry reopens the writer, which truncates and restarts the
    download cleanly.
    """
    url = f"{BASE}/data/{flow}/all"
    client = get_client()
    with client.stream(
        "GET",
        url,
        headers={"Accept": CSV_ACCEPT},
        timeout=httpx.Timeout(600.0, connect=60.0),
    ) as resp:
        resp.raise_for_status()
        reader = csv.reader(resp.iter_lines())
        header = next(reader, None)
        if not header:
            raise ValueError(f"{flow}: empty SDMX-CSV response (no header)")
        header[0] = header[0].lstrip("﻿")  # strip a possible BOM
        with raw_writer(asset, RAW_EXT, mode="wt", compression="gzip") as out:
            for row in reader:
                rec = dict(zip(header, row))
                out.write(json.dumps(rec) + "\n")


def fetch_one(node_id: str) -> None:
    asset = node_id  # the runtime passes the spec id; it IS the asset name
    flow = SPEC_TO_FLOW[node_id]
    _download_cube(flow, asset)


DOWNLOAD_SPECS = [
    NodeSpec(id=_spec_id(e), fn=fetch_one, kind="download")
    for e in ENTITY_IDS
]
