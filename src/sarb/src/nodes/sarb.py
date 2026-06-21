"""SARB (South African Reserve Bank) connector.

Source surface — the SARB Web API (custom.resbank.co.za/SarbWebApi), a public
ASP.NET Web API returning JSON, no auth:

  * WebIndicators/ReleaseOfSelectedData lists the release groups ("DataType"s):
    Money and banking, Banks and mutual banks, International economic data,
    National government finance, Capital market, Economic indicators, the MRG*
    graph variants, and the CDA* credit/deposit/securitisation detail.
  * WebIndicators/ReleaseOfSelectedData/MonthlyIndicatorsAll/{dataType} returns
    that group's COMPLETE historical time series in one call — a flat array of
    {TimeSeriesCode, MeasureName, CategoryCode, CategoryName, DataType,
     SubTitle, Period, Value, Description, FormatNumber, FormatDate}. Value is a
    locale-formatted string (decimal comma, non-breaking-space thousands sep);
    Period is "YYYY/MM/DD HH:MM:SS".

Every observation in every group shares ONE schema, so this is the flat
time-series shape: a single long-format `values` subset, with the release group
(data_type) and series id (timeseries_code) as columns.

Fetch shape: stateless full re-pull. Each MonthlyIndicatorsAll call returns the
whole history for its group (no incremental filter exists), the full corpus is
small (low hundreds of thousands of rows total), and re-pulling each run picks
up revisions for free. The group list is discovered live from
ReleaseOfSelectedData — never hardcoded. Raw is streamed one group at a time
via raw_parquet_writer so memory stays bounded regardless of corpus growth.
"""

import httpx
import pyarrow as pa

from subsets_utils import (
    NodeSpec,
    SqlNodeSpec,
    get,
    raw_parquet_writer,
    transient_retry,
)

_BASE = "https://custom.resbank.co.za/SarbWebApi/WebIndicators"
_RELEASES_URL = f"{_BASE}/ReleaseOfSelectedData"

# custom.resbank.co.za is slow and the bulk payloads are large; give the read
# phase plenty of headroom (the wrapper's default 30s is too short).
_TIMEOUT = httpx.Timeout(connect=15.0, read=300.0, write=60.0, pool=60.0)

# Faithful raw schema — every field stored as the source's string, typed in the
# transform. Mark all nullable: SubTitle/Description are routinely blank/null.
_SCHEMA = pa.schema([
    ("timeseries_code", pa.string()),
    ("measure_name", pa.string()),
    ("category_code", pa.string()),
    ("category_name", pa.string()),
    ("data_type", pa.string()),
    ("sub_title", pa.string()),
    ("period", pa.string()),
    ("value", pa.string()),
    ("description", pa.string()),
    ("format_number", pa.string()),
    ("format_date", pa.string()),
])


@transient_retry()
def _fetch_json(url: str):
    resp = get(url, timeout=_TIMEOUT)
    resp.raise_for_status()
    return resp.json()


def _rows_to_table(records: list) -> pa.Table:
    """Project the source records onto the faithful string schema."""
    cols = {name: [] for name in _SCHEMA.names}
    for r in records:
        cols["timeseries_code"].append(r.get("TimeSeriesCode"))
        cols["measure_name"].append(r.get("MeasureName"))
        cols["category_code"].append(r.get("CategoryCode"))
        cols["category_name"].append(r.get("CategoryName"))
        cols["data_type"].append(r.get("DataType"))
        cols["sub_title"].append(r.get("SubTitle"))
        cols["period"].append(r.get("Period"))
        # Value is numeric-as-string; keep it verbatim, type it in the transform.
        v = r.get("Value")
        cols["value"].append(None if v is None else str(v))
        cols["description"].append(r.get("Description"))
        cols["format_number"].append(r.get("FormatNumber"))
        cols["format_date"].append(r.get("FormatDate"))
    return pa.table(cols, schema=_SCHEMA)


def fetch_values(node_id: str) -> None:
    """Re-pull every SARB release group and stream them into one raw asset.

    Discovers the release groups from ReleaseOfSelectedData, then fetches each
    group's full history from MonthlyIndicatorsAll/{dataType}. One parquet asset
    (`node_id`) holds the union of all groups; the group is a column.
    """
    asset = node_id

    releases = _fetch_json(_RELEASES_URL)
    if not isinstance(releases, list) or not releases:
        raise RuntimeError(f"ReleaseOfSelectedData returned no groups: {releases!r}")
    data_types = [r["DataType"] for r in releases if r.get("DataType")]
    if not data_types:
        raise RuntimeError("ReleaseOfSelectedData carried no DataType ids")

    total = 0
    with raw_parquet_writer(asset, _SCHEMA) as writer:
        for dt in data_types:
            records = _fetch_json(f"{_RELEASES_URL}/MonthlyIndicatorsAll/{dt}")
            if not isinstance(records, list):
                raise RuntimeError(f"{dt}: expected a JSON array, got {type(records)}")
            if not records:
                # An empty group is unexpected (every listed group has history);
                # surface it rather than silently shrinking the corpus.
                raise RuntimeError(f"{dt}: MonthlyIndicatorsAll returned 0 records")
            writer.write_table(_rows_to_table(records))
            total += len(records)

    print(f"  -> {asset}: {total} observations across {len(data_types)} release groups")


DOWNLOAD_SPECS = [
    NodeSpec(id="sarb-values", fn=fetch_values, kind="download"),
]


# Long-format observations. Strip the locale formatting (non-breaking-space /
# space thousands separators, decimal comma) and type Value/Period; drop rows
# that don't parse; de-dup defensively on (data_type, series, date). The source
# SubTitle field is always blank, so it is not published.
TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="sarb-values-transform",
        deps=["sarb-values"],
        sql=r'''
            WITH cleaned AS (
                SELECT
                    TRY_CAST(strptime(period, '%Y/%m/%d %H:%M:%S') AS DATE) AS date,
                    timeseries_code,
                    measure_name,
                    category_code,
                    category_name,
                    data_type,
                    TRY_CAST(
                        replace(replace(replace(value, chr(160), ''), ' ', ''), ',', '.')
                        AS DOUBLE
                    ) AS value
                FROM "sarb-values"
            )
            SELECT date, timeseries_code, measure_name, category_code,
                   category_name, data_type, value
            FROM cleaned
            WHERE date IS NOT NULL
              AND value IS NOT NULL
              AND timeseries_code IS NOT NULL
            QUALIFY row_number() OVER (
                PARTITION BY data_type, timeseries_code, date
                ORDER BY measure_name
            ) = 1
        ''',
    ),
]
