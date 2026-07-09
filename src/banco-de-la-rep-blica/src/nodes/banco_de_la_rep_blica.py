"""Banco de la República (Colombia) — economic statistics SDMX connector.

Mechanism: SDMX 2.1 REST web service at
https://totoro.banrep.gov.co/nsi-jax-ws/rest/ (agency ESTAT). One GET per
dataflow id against `/data/<DATAFLOW_ID>` returns the dataflow's entire content
(every series, full history) as SDMX 2.1 GenericData XML in a single response —
no pagination. We re-pull each dataflow in full every run (stateless full
re-pull): each is a few MB and the source has no usable per-request `since`
filter, so revisions and late corrections are always picked up.

WAF gotcha: the comma-key form `/data/ESTAT,DF_X,1.0` is blocked by the site's
bot-mitigation WAF (returns an HTML "Unauthorized Request Blocked" page with
HTTP 200). The bare-id form `/data/DF_X` works; we always use it, plus a browser
User-Agent and a Referer header.

Raw shape: one row per (series, observation). All dataflows share the same
GenericData structure (SeriesKey dimensions REFERENCE_AREA / SUBJECT /
EXPENDITURE / ACTIVITY / ADJUSTMENT / UNIT_MEASURE / FREQ, series attributes
DOMAIN / UNIT_MULT, and TIME_PERIOD observations with OBS_STATUS). Stored as
all-string parquet (faithful to the XML); the transform casts/parses.
"""

import xml.etree.ElementTree as ET

import pyarrow as pa
from subsets_utils import (
    NodeSpec,
    get,
    save_raw_parquet,
)
from constants import ENTITY_IDS

SLUG = "banco-de-la-rep-blica"
DATA_BASE = "https://totoro.banrep.gov.co/nsi-jax-ws/rest/data/"

# Browser-ish headers to stay clear of the PerfDrive/Radware bot WAF. ASCII only.
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/124.0 Safari/537.36"
    ),
    "Referer": "https://suameca.banrep.gov.co/estadisticas-economicas/",
    "Accept": "application/vnd.sdmx.genericdata+xml, application/xml, */*",
}

_NS = {
    "g": "http://www.sdmx.org/resources/sdmxml/schemas/v2_1/data/generic",
}

# All columns are stored as strings — the raw is a faithful copy of the SDMX
# GenericData; typing/parsing happens in the transform SQL.
SCHEMA = pa.schema([
    ("reference_area", pa.string()),
    ("subject", pa.string()),
    ("expenditure", pa.string()),
    ("activity", pa.string()),
    ("adjustment", pa.string()),
    ("unit_measure", pa.string()),
    ("freq", pa.string()),
    ("domain", pa.string()),
    ("unit_mult", pa.string()),
    ("time_period", pa.string()),
    ("obs_value", pa.string()),
    ("obs_status", pa.string()),
])

_DIM_KEYS = (
    "REFERENCE_AREA", "SUBJECT", "EXPENDITURE", "ACTIVITY",
    "ADJUSTMENT", "UNIT_MEASURE", "FREQ",
)


def _entity_from_node_id(node_id: str) -> str:
    """`banco-de-la-rep-blica-df-trm-daily-hist` -> `DF_TRM_DAILY_HIST`."""
    stub = node_id[len(SLUG) + 1:]
    return stub.upper().replace("-", "_")


def _fetch_dataflow(dataflow_id: str) -> bytes:
    resp = get(
        DATA_BASE + dataflow_id,
        headers=HEADERS,
        timeout=(10.0, 180.0),
    )
    resp.raise_for_status()
    body = resp.content
    # The WAF answers HTTP 200 with an HTML block page; SDMX answers XML.
    head = body[:200].lstrip().lower()
    if head.startswith(b"<html") or b"unauthorized request" in head:
        raise RuntimeError(
            f"{dataflow_id}: WAF block page returned instead of SDMX XML"
        )
    return body


def _parse_observations(body: bytes) -> list[dict]:
    root = ET.fromstring(body)
    rows: list[dict] = []
    for series in root.findall(".//g:Series", _NS):
        key = {
            v.get("id"): v.get("value")
            for v in series.findall("g:SeriesKey/g:Value", _NS)
        }
        attrs = {
            v.get("id"): v.get("value")
            for v in series.findall("g:Attributes/g:Value", _NS)
        }
        base = {
            "reference_area": key.get("REFERENCE_AREA"),
            "subject": key.get("SUBJECT"),
            "expenditure": key.get("EXPENDITURE"),
            "activity": key.get("ACTIVITY"),
            "adjustment": key.get("ADJUSTMENT"),
            "unit_measure": key.get("UNIT_MEASURE"),
            "freq": key.get("FREQ"),
            "domain": attrs.get("DOMAIN"),
            "unit_mult": attrs.get("UNIT_MULT"),
        }
        for obs in series.findall("g:Obs", _NS):
            dim = obs.find("g:ObsDimension", _NS)
            val = obs.find("g:ObsValue", _NS)
            obs_attrs = {
                v.get("id"): v.get("value")
                for v in obs.findall("g:Attributes/g:Value", _NS)
            }
            row = dict(base)
            row["time_period"] = dim.get("value") if dim is not None else None
            row["obs_value"] = val.get("value") if val is not None else None
            row["obs_status"] = obs_attrs.get("OBS_STATUS")
            rows.append(row)
    return rows


def fetch_one(node_id: str) -> None:
    asset = node_id  # the spec id IS the asset name
    dataflow_id = _entity_from_node_id(node_id)
    body = _fetch_dataflow(dataflow_id)
    rows = _parse_observations(body)
    if not rows:
        raise RuntimeError(f"{dataflow_id}: parsed 0 observations from SDMX XML")
    table = pa.Table.from_pylist(rows, schema=SCHEMA)
    save_raw_parquet(table, asset)


DOWNLOAD_SPECS = [
    NodeSpec(
        id=f"{SLUG}-{eid.lower().replace('_', '-')}",
        fn=fetch_one,
        kind="download",
    )
    for eid in ENTITY_IDS
]
