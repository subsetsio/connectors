"""WHO GHO raw downloads."""

import logging

import httpx
import pyarrow as pa

from subsets_utils import NodeSpec, raw_parquet_writer, save_raw_parquet
from utils import BASE, fetch_odata

log = logging.getLogger("who")


_INDICATOR_SCHEMA = pa.schema(
    [
        ("IndicatorCode", pa.string()),
        ("IndicatorName", pa.string()),
        ("Language", pa.string()),
    ]
)

_DIMENSION_SCHEMA = pa.schema(
    [
        ("DimensionCode", pa.string()),
        ("DimensionTitle", pa.string()),
        ("Code", pa.string()),
        ("Title", pa.string()),
        ("ParentDimension", pa.string()),
        ("ParentCode", pa.string()),
        ("ParentTitle", pa.string()),
    ]
)

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

_STR_COLS = [f.name for f in _VALUES_SCHEMA if f.type == pa.string()]
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


def _is_permanent_client_error(e: httpx.HTTPStatusError) -> bool:
    code = e.response.status_code
    return 400 <= code < 500 and code != 429


def fetch_dimensions(node_id: str) -> None:
    dims = fetch_odata(f"{BASE}/Dimension")
    if not dims:
        raise RuntimeError("WHO /Dimension returned no rows")
    log.info("who-dimensions: resolving values for %d dimensions", len(dims))

    rows: list[dict] = []
    skipped: list[str] = []
    for d in dims:
        code = d.get("Code")
        if not code:
            continue
        try:
            values = fetch_odata(f"{BASE}/DIMENSION/{code}/DimensionValues")
        except httpx.HTTPStatusError as e:
            # A handful of dimension codes are listed but expose no value endpoint.
            if _is_permanent_client_error(e):
                log.warning(
                    "who-dimensions: skipping %s (HTTP %s)", code, e.response.status_code
                )
                skipped.append(code)
                continue
            raise
        for v in values:
            rows.append(
                {
                    "DimensionCode": code,
                    "DimensionTitle": _to_str(d.get("Title")),
                    "Code": _to_str(v.get("Code")),
                    "Title": _to_str(v.get("Title")),
                    "ParentDimension": _to_str(v.get("ParentDimension")),
                    "ParentCode": _to_str(v.get("ParentCode")),
                    "ParentTitle": _to_str(v.get("ParentTitle")),
                }
            )

    if not rows:
        raise RuntimeError("who-dimensions: crawl produced zero dimension values")
    table = pa.Table.from_pylist(rows, schema=_DIMENSION_SCHEMA)
    save_raw_parquet(table, node_id)
    log.info(
        "who-dimensions: wrote %d values across %d dimensions (%d skipped)",
        table.num_rows,
        len(dims) - len(skipped),
        len(skipped),
    )


def fetch_indicators(node_id: str) -> None:
    rows = fetch_odata(f"{BASE}/Indicator")
    if not rows:
        raise RuntimeError("WHO /Indicator returned no rows")

    norm = [
        {
            "IndicatorCode": r.get("IndicatorCode"),
            "IndicatorName": r.get("IndicatorName"),
            "Language": r.get("Language"),
        }
        for r in rows
    ]
    table = pa.Table.from_pylist(norm, schema=_INDICATOR_SCHEMA)
    save_raw_parquet(table, node_id)
    log.info("who-indicators: wrote %d indicators", table.num_rows)


def fetch_values(node_id: str) -> None:
    indicators = fetch_odata(f"{BASE}/Indicator")
    codes = sorted({r["IndicatorCode"] for r in indicators if r.get("IndicatorCode")})
    if not codes:
        raise RuntimeError("WHO /Indicator returned no indicator codes")
    log.info("who-values: crawling %d indicators", len(codes))

    total = 0
    skipped: list[str] = []
    with raw_parquet_writer(node_id, _VALUES_SCHEMA) as writer:
        for i, code in enumerate(codes):
            try:
                rows = fetch_odata(f"{BASE}/{code}")
            except httpx.HTTPStatusError as e:
                # Permanent client errors can occur for withdrawn indicator codes.
                if _is_permanent_client_error(e):
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
    NodeSpec(id="who-dimensions", fn=fetch_dimensions, kind="download"),
    NodeSpec(id="who-indicators", fn=fetch_indicators, kind="download"),
    NodeSpec(id="who-values", fn=fetch_values, kind="download"),
]
