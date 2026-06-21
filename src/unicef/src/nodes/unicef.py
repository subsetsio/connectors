"""UNICEF Indicator Data Warehouse connector (SDMX 2.1).

One download per in-scope dataflow: the full SDMX-CSV table is streamed from
the public warehouse and normalized to a uniform tidy long schema (universal
observation fields + a `dimensions` JSON blob preserving every other
disaggregation the dataflow carries). One SQL transform per dataflow publishes
that tidy table as a Delta table.

Access: https://sdmx.data.unicef.org/ws/public/sdmxapi/rest/data/{agency},{flow},{version}/?format=csv
No auth. Full-corpus re-pull each refresh (stateless) — SDMX supports
`updatedAfter` for deltas but our pattern is whole-source snapshots and the
warehouse is small enough (largest flows ~hundreds of MB) to re-pull. Rows are
streamed to disk so memory stays bounded regardless of flow size.
"""
import csv
import json
import re

import pyarrow as pa

from subsets_utils import (
    NodeSpec,
    SqlNodeSpec,
    get_client,
    raw_parquet_writer,
    transient_retry,
)

BASE = "https://sdmx.data.unicef.org/ws/public/sdmxapi/rest/data"

# Rows are streamed to parquet in fixed-size batches so memory stays bounded
# regardless of flow size (the largest flows exceed 8M observations).
_BATCH_ROWS = 50_000

# Uniform tidy schema for every dataflow. All values are strings as they arrive
# in SDMX-CSV; the transform TRY_CASTs the numeric ones. Parquet (columnar,
# compressed, streamable by DuckDB) keeps transform memory far below the JSON
# parse spike that NDJSON incurs on the multi-million-row flows.
_FIELDS = [
    "ref_area", "ref_area_name", "indicator", "indicator_name",
    "sex", "age", "time_period", "obs_value", "unit_measure",
    "obs_status", "data_source", "lower_bound", "upper_bound", "dimensions",
]
SCHEMA = pa.schema([(f, pa.string()) for f in _FIELDS])

# The entity union — every rank-active dataflow, "AGENCY:FLOW:VERSION".
from constants import ENTITY_IDS


def _spec_id(entity_id: str) -> str:
    return "unicef-" + entity_id.lower().replace("_", "-")


# Header-name aliases for the universal tidy columns. SDMX-CSV emits a code
# column (UPPER_CASE) immediately followed by a human-label column; we pull a
# small set of universal fields by name and preserve everything else as JSON.
_REF_AREA_CODE = ("REF_AREA",)
_REF_AREA_NAME = ("Geographic area", "Reference area", "Country")
_INDICATOR_CODE = ("INDICATOR", "SERIES")
_INDICATOR_NAME = ("Indicator", "SDG Series", "Series Name")
_SEX = ("SEX",)
_AGE = ("AGE", "AGE_GROUP", "CURRENT_AGE")
_TIME = ("TIME_PERIOD",)
_OBS = ("OBS_VALUE",)
_UNIT = ("UNIT_MEASURE",)
_STATUS = ("OBS_STATUS",)
_SOURCE = ("DATA_SOURCE",)
_LOWER = ("LOWER_BOUND",)
_UPPER = ("UPPER_BOUND",)

# Code columns already surfaced as their own tidy field — excluded from the
# `dimensions` JSON blob to avoid duplication.
_PROMOTED_CODES = {
    "REF_AREA", "INDICATOR", "SERIES", "SEX", "AGE", "TIME_PERIOD",
    "OBS_VALUE", "UNIT_MEASURE", "OBS_STATUS", "DATA_SOURCE",
    "LOWER_BOUND", "UPPER_BOUND",
}
_CODE_COL = re.compile(r"^[A-Z][A-Z0-9_]*$")


def _first(row_by_header: dict, names) -> str | None:
    for n in names:
        v = row_by_header.get(n)
        if v not in (None, ""):
            return v
    return None


def _normalize(header: list[str], values: list[str]) -> dict:
    """Map one SDMX-CSV row to the uniform tidy record."""
    d = {}
    for h, v in zip(header, values):
        if h not in d:  # keep first occurrence of a header
            d[h] = v
    # Preserve every remaining code dimension/attribute as a JSON blob.
    dims = {
        h: v
        for h, v in d.items()
        if v not in (None, "") and _CODE_COL.match(h) and h not in _PROMOTED_CODES
    }
    return {
        "ref_area": _first(d, _REF_AREA_CODE),
        "ref_area_name": _first(d, _REF_AREA_NAME),
        "indicator": _first(d, _INDICATOR_CODE),
        "indicator_name": _first(d, _INDICATOR_NAME),
        "sex": _first(d, _SEX),
        "age": _first(d, _AGE),
        "time_period": _first(d, _TIME),
        "obs_value": _first(d, _OBS),
        "unit_measure": _first(d, _UNIT),
        "obs_status": _first(d, _STATUS),
        "data_source": _first(d, _SOURCE),
        "lower_bound": _first(d, _LOWER),
        "upper_bound": _first(d, _UPPER),
        "dimensions": json.dumps(dims, ensure_ascii=False) if dims else None,
    }


def _flush(writer, batch: list[dict]) -> None:
    writer.write_table(pa.Table.from_pylist(batch, schema=SCHEMA))


@transient_retry()
def _stream_csv_to_parquet(url: str, asset: str) -> int:
    """Stream the dataflow CSV and write normalized parquet. Returns row count."""
    client = get_client()
    written = 0
    with client.stream(
        "GET", url, params={"format": "csv"}, timeout=(10.0, 600.0)
    ) as resp:
        resp.raise_for_status()
        # iter_lines yields decoded text lines; csv.reader re-joins quoted
        # fields that span lines (SDMX labels can contain embedded newlines).
        reader = csv.reader(resp.iter_lines())
        header = next(reader, None)
        if not header:
            return 0
        with raw_parquet_writer(asset, SCHEMA) as writer:
            batch: list[dict] = []
            for values in reader:
                if not values:
                    continue
                batch.append(_normalize(header, values))
                written += 1
                if len(batch) >= _BATCH_ROWS:
                    _flush(writer, batch)
                    batch = []
            if batch:
                _flush(writer, batch)
    return written


def fetch_one(node_id: str) -> None:
    asset = node_id  # the spec id IS the asset name
    # Recover the source entity (AGENCY:FLOW:VERSION) from the spec id.
    entity = next((e for e in ENTITY_IDS if _spec_id(e) == node_id), None)
    if entity is None:
        raise ValueError(f"no entity union member maps to spec id {node_id!r}")
    agency, flow, version = entity.split(":")
    url = f"{BASE}/{agency},{flow},{version}/"
    n = _stream_csv_to_parquet(url, asset)
    if n == 0:
        raise ValueError(f"{asset}: dataflow {entity} returned 0 observations")


DOWNLOAD_SPECS = [
    NodeSpec(id=_spec_id(eid), fn=fetch_one, kind="download")
    for eid in ENTITY_IDS
]


# One tidy Delta table per dataflow. The schema is uniform across every flow:
# universal observation fields plus the preserved `dimensions` JSON.
_TRANSFORM_SQL = '''
    SELECT
        ref_area,
        ref_area_name,
        indicator,
        indicator_name,
        sex,
        age,
        time_period,
        TRY_CAST(obs_value AS DOUBLE)  AS obs_value,
        obs_value                       AS obs_value_raw,
        unit_measure,
        obs_status,
        data_source,
        TRY_CAST(lower_bound AS DOUBLE) AS lower_bound,
        TRY_CAST(upper_bound AS DOUBLE) AS upper_bound,
        dimensions
    FROM "{dep}"
    WHERE obs_value IS NOT NULL AND obs_value <> ''
'''

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id=f"{s.id}-transform",
        deps=[s.id],
        sql=_TRANSFORM_SQL.format(dep=s.id),
    )
    for s in DOWNLOAD_SPECS
]
