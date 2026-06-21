"""who-values — long-format observations across every WHO GHO indicator.

Subset: who-values — one request per indicator returns its full series; we crawl
all indicators (codes from /Indicator) and stream them to one parquet asset.
A per-indicator permanent error is logged and skipped so one bad indicator never
sinks the whole crawl.
"""

import logging

import httpx
import pyarrow as pa

from subsets_utils import NodeSpec, SqlNodeSpec, raw_parquet_writer
from utils import BASE, fetch_odata

log = logging.getLogger("who")


# Raw fidelity: every column kept as string except the four numeric measures.
# Year/timestamps stay textual here and are cast in the transform SQL.
_VALUES_SCHEMA = pa.schema(
    [
        ("Id", pa.int64()),
        ("IndicatorCode", pa.string()),
        ("SpatialDimType", pa.string()),
        ("SpatialDim", pa.string()),
        ("ParentLocationCode", pa.string()),
        ("ParentLocation", pa.string()),
        ("TimeDimType", pa.string()),
        ("TimeDim", pa.string()),
        ("TimeDimensionValue", pa.string()),
        ("TimeDimensionBegin", pa.string()),
        ("TimeDimensionEnd", pa.string()),
        ("Dim1Type", pa.string()),
        ("Dim1", pa.string()),
        ("Dim2Type", pa.string()),
        ("Dim2", pa.string()),
        ("Dim3Type", pa.string()),
        ("Dim3", pa.string()),
        ("DataSourceDimType", pa.string()),
        ("DataSourceDim", pa.string()),
        ("Value", pa.string()),
        ("NumericValue", pa.float64()),
        ("Low", pa.float64()),
        ("High", pa.float64()),
        ("Comments", pa.string()),
        ("Date", pa.string()),
    ]
)

_STR_COLS = [
    f.name for f in _VALUES_SCHEMA if f.type == pa.string()
]
_FLOAT_COLS = ["NumericValue", "Low", "High"]


def _to_str(v):
    return None if v is None else str(v)


def _to_float(v):
    if v is None or v == "":
        return None
    try:
        return float(v)
    except (TypeError, ValueError):
        return None


def _normalize_value_row(r: dict) -> dict:
    out = {}
    out["Id"] = int(r["Id"]) if r.get("Id") is not None else None
    for c in _STR_COLS:
        out[c] = _to_str(r.get(c))
    for c in _FLOAT_COLS:
        out[c] = _to_float(r.get(c))
    return out


def fetch_values(node_id: str) -> None:
    asset = node_id
    indicators = fetch_odata(f"{BASE}/Indicator")
    codes = sorted({r["IndicatorCode"] for r in indicators if r.get("IndicatorCode")})
    if not codes:
        raise RuntimeError("WHO /Indicator returned no indicator codes")
    log.info("who-values: crawling %d indicators", len(codes))

    total = 0
    skipped: list[str] = []
    with raw_parquet_writer(asset, _VALUES_SCHEMA) as writer:
        for i, code in enumerate(codes):
            try:
                rows = fetch_odata(f"{BASE}/{code}")
            except httpx.HTTPStatusError as e:
                # Permanent client errors (e.g. 404 for a withdrawn code): skip,
                # don't sink the whole crawl. Transient errors already retried.
                if e.response.status_code == 404 or (
                    400 <= e.response.status_code < 500
                    and e.response.status_code != 429
                ):
                    log.warning("who-values: skipping %s (HTTP %s)", code, e.response.status_code)
                    skipped.append(code)
                    continue
                raise
            if not rows:
                continue
            batch = pa.RecordBatch.from_pylist(
                [_normalize_value_row(r) for r in rows], schema=_VALUES_SCHEMA
            )
            writer.write_batch(batch)
            total += batch.num_rows
            if (i + 1) % 250 == 0:
                log.info("who-values: %d/%d indicators, %d rows", i + 1, len(codes), total)

    if total == 0:
        raise RuntimeError("who-values: crawl produced zero observations")
    log.info(
        "who-values: wrote %d observations from %d indicators (%d skipped)",
        total,
        len(codes) - len(skipped),
        len(skipped),
    )


DOWNLOAD_SPECS = [
    NodeSpec(id="who-values", fn=fetch_values, kind="download"),
]


TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="who-values-transform",
        deps=["who-values"],
        sql='''
            SELECT
                CAST(Id AS BIGINT)              AS observation_id,
                IndicatorCode                   AS indicator_code,
                SpatialDimType                  AS spatial_dim_type,
                SpatialDim                      AS spatial_dim,
                ParentLocationCode              AS parent_location_code,
                ParentLocation                  AS parent_location,
                TimeDimType                     AS time_dim_type,
                TRY_CAST(TimeDim AS INTEGER)    AS year,
                TimeDim                         AS time_dim,
                Dim1Type                        AS dim1_type,
                Dim1                            AS dim1,
                Dim2Type                        AS dim2_type,
                Dim2                            AS dim2,
                Dim3Type                        AS dim3_type,
                Dim3                            AS dim3,
                DataSourceDim                   AS data_source,
                Value                           AS value_display,
                NumericValue                    AS numeric_value,
                Low                             AS low,
                High                            AS high,
                Comments                        AS comments,
                TRY_CAST(Date AS TIMESTAMP)     AS updated_at
            FROM "who-values"
            WHERE Id IS NOT NULL
        ''',
    ),
]
