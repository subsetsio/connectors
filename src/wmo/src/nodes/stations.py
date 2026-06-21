"""wmo-stations — the series catalog.

One row per timeseries: provider, station, variable, unit, cadence, period of
record. Fed by the GEO-DAB timeseries-api JSON endpoint with includeData=false
(metadata only) — fast and reliable.

Deterministic, stateless scope: every WHOS provider's full series catalog,
walked in sorted provider order. No wall-clock budget — per-request timeouts
bound slow providers and the supervisor bounds the run.
"""

import httpx
import pyarrow as pa

from subsets_utils import (
    NodeSpec,
    SqlNodeSpec,
    raw_parquet_writer,
)
from utils import (
    META_PAGE,
    _list_providers,
    _members,
    _parse_dt,
)

_STATIONS_SCHEMA = pa.schema([
    ("provider", pa.string()),
    ("timeseries_id", pa.string()),
    ("station_id", pa.string()),
    ("variable_code", pa.string()),
    ("variable_name", pa.string()),
    ("unit", pa.string()),
    ("aggregation", pa.string()),
    ("interpolation", pa.string()),
    ("period_begin", pa.timestamp("s", tz="UTC")),
    ("period_end", pa.timestamp("s", tz="UTC")),
])


# --------------------------------------------------------------------------- #
# stations — series catalog from the (fast) metadata endpoint
# --------------------------------------------------------------------------- #

def _station_rows(provider, members) -> list[dict]:
    rows = []
    for m in members:
        result = m.get("result") or {}
        dpm = result.get("defaultPointMetadata") or {}
        op = m.get("observedProperty") or {}
        foi = m.get("featureOfInterest") or {}
        ptime = m.get("phenomenonTime") or {}
        interp = dpm.get("interpolationType") or {}
        rows.append({
            "provider": provider,
            "timeseries_id": m.get("id"),
            "station_id": foi.get("href"),
            "variable_code": op.get("href"),
            "variable_name": op.get("title"),
            "unit": dpm.get("uom"),
            "aggregation": dpm.get("aggregationDuration"),
            "interpolation": interp.get("title"),
            "period_begin": _parse_dt(ptime.get("begin")),
            "period_end": _parse_dt(ptime.get("end")),
        })
    return rows


def _write_provider_stations(asset_id, provider) -> None:
    """Stream one provider's full series catalog to a parquet batch."""
    writer_cm = None
    writer = None
    offset = 1
    try:
        while True:
            members = _members(provider, offset, META_PAGE)
            rows = _station_rows(provider, members)
            if rows:
                table = pa.Table.from_pylist(rows, schema=_STATIONS_SCHEMA)
                if writer is None:
                    writer_cm = raw_parquet_writer(asset_id, _STATIONS_SCHEMA)
                    writer = writer_cm.__enter__()
                writer.write_table(table)
            if len(members) < META_PAGE:
                break
            offset += META_PAGE
    finally:
        if writer_cm is not None:
            writer_cm.__exit__(None, None, None)


def fetch_stations(node_id: str) -> None:
    asset = node_id  # "wmo-stations"

    try:
        providers = _list_providers()
    except httpx.HTTPError as exc:
        print(f"[wmo-stations] provider enumeration failed: {type(exc).__name__}")
        return

    # Deterministic scope: every provider's full series catalog. No time cap —
    # request timeouts bound slow providers and the supervisor bounds the run.
    for provider in providers:
        try:
            _write_provider_stations(f"{asset}-{provider}", provider)
        except httpx.HTTPError as exc:
            print(f"[wmo-stations] skip provider {provider}: {type(exc).__name__}")
            continue


DOWNLOAD_SPECS = [
    NodeSpec(id="wmo-stations", fn=fetch_stations, kind="download"),
]

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="wmo-stations-transform",
        deps=["wmo-stations"],
        sql='''
            SELECT DISTINCT
                provider,
                timeseries_id,
                station_id,
                variable_code,
                variable_name,
                unit,
                aggregation,
                interpolation,
                CAST(period_begin AS TIMESTAMP) AS period_begin,
                CAST(period_end   AS TIMESTAMP) AS period_end
            FROM "wmo-stations"
            WHERE timeseries_id IS NOT NULL
        ''',
    ),
]
