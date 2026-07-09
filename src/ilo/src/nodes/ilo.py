"""ILO (ILOSTAT) connector.

Downloads one gzipped tidy CSV per accepted ILOSTAT indicator-frequency dataset
from the public rplumber bulk facility and normalizes each payload to a fixed
parquet schema. Transforms are authored in src/transforms by the transform
stage; this module intentionally exposes only DOWNLOAD_SPECS.
"""
import csv
import gzip
import io
import time

import pyarrow as pa

from constants import ENTITY_IDS
from subsets_utils import NodeSpec, get, save_raw_parquet

DATA_URL = "https://rplumber.ilo.org/data/indicator"

_BAD_REQUEST_ATTEMPTS = 3
_BAD_REQUEST_BACKOFF_S = 5.0

RAW_SCHEMA = pa.schema([
    ("ref_area", pa.string()),
    ("source", pa.string()),
    ("indicator", pa.string()),
    ("sex", pa.string()),
    ("classif1", pa.string()),
    ("classif2", pa.string()),
    ("time_period", pa.string()),
    ("obs_value", pa.float64()),
    ("obs_status", pa.string()),
])



def _entity_from_node(node_id: str) -> str:
    return node_id.removeprefix("ilo-").upper().replace("-", "_")


def _to_float(value: str | None) -> float | None:
    if value is None or value == "":
        return None
    try:
        return float(value)
    except ValueError:
        return None


def _fetch_csv_gz(entity_id: str):
    """rplumber answers a perfectly valid indicator id with 400 when it is busy
    — six of them did so in run 20260707-114522 and all six serve 200 on retry.
    The shared client retries 429/5xx only, so absorb the spurious 400 here."""
    for attempt in range(_BAD_REQUEST_ATTEMPTS):
        resp = get(
            DATA_URL,
            params={"id": entity_id, "format": ".csv.gz"},
            timeout=(10.0, 180.0),
        )
        if resp.status_code != 400 or attempt == _BAD_REQUEST_ATTEMPTS - 1:
            return resp
        time.sleep(_BAD_REQUEST_BACKOFF_S * 2 ** attempt)


def fetch_one(node_id: str) -> None:
    entity_id = _entity_from_node(node_id)
    resp = _fetch_csv_gz(entity_id)
    resp.raise_for_status()
    text = gzip.decompress(resp.content).decode("utf-8-sig")
    reader = csv.DictReader(io.StringIO(text))

    columns = {
        "ref_area": [],
        "source": [],
        "indicator": [],
        "sex": [],
        "classif1": [],
        "classif2": [],
        "time_period": [],
        "obs_value": [],
        "obs_status": [],
    }
    for row in reader:
        columns["ref_area"].append(row.get("ref_area"))
        columns["source"].append(row.get("source"))
        columns["indicator"].append(row.get("indicator"))
        columns["sex"].append(row.get("sex"))
        columns["classif1"].append(row.get("classif1"))
        columns["classif2"].append(row.get("classif2"))
        columns["time_period"].append(row.get("time"))
        columns["obs_value"].append(_to_float(row.get("obs_value")))
        columns["obs_status"].append(row.get("obs_status"))

    table = pa.table(
        {
            "ref_area": pa.array(columns["ref_area"], pa.string()),
            "source": pa.array(columns["source"], pa.string()),
            "indicator": pa.array(columns["indicator"], pa.string()),
            "sex": pa.array(columns["sex"], pa.string()),
            "classif1": pa.array(columns["classif1"], pa.string()),
            "classif2": pa.array(columns["classif2"], pa.string()),
            "time_period": pa.array(columns["time_period"], pa.string()),
            "obs_value": pa.array(columns["obs_value"], pa.float64()),
            "obs_status": pa.array(columns["obs_status"], pa.string()),
        },
        schema=RAW_SCHEMA,
    )
    save_raw_parquet(table, node_id)


DOWNLOAD_SPECS = [
    NodeSpec(
        id=f"ilo-{entity_id.lower().replace('_', '-')}",
        fn=fetch_one,
        kind="download",
    )
    for entity_id in ENTITY_IDS
]
