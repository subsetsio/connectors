"""Climate TRACE connector — greenhouse-gas emissions.

Two published subsets, both sourced from the Climate TRACE bulk country packages
(`downloads.climatetrace.org/latest/country_packages/{gas}/{ISO3}.zip`):

  - country_emissions : country x sector x subsector x year emissions time series
  - asset_emissions   : geolocated facility/source-level emissions

Gas scope: **co2e_100yr** — all greenhouse gases combined, expressed as
CO2-equivalent using 100-year global-warming potentials. This is Climate TRACE's
headline, fully-comparable metric and is the ONLY gas whose country packages
cover all 10 sectors (the per-gas co2/ch4/n2o packages and the co2e sector
packages are sector-incomplete). Other gases are reachable via the same
mechanism by swapping the `{gas}` path segment; deferred for scope.

Fetch shape: stateless full re-pull (decision shape 1). `latest/` is repointed
each (~monthly) release, the packages carry no incremental delta, and the whole
co2e_100yr corpus is only a few GB — so every run re-fetches the full corpus and
overwrites. No watermark/cursor. The country list is enumerated at run time from
the v6 definitions API (per research's download_handoff) rather than the cached,
1000-key-truncated S3 listing.

Each country zip is streamed to a temp file (bounded memory), opened, and only
the CSV members we need are parsed:
  - <subsector>_country_emissions_v*.csv  -> country_emissions
  - <subsector>_emissions_sources_v*.csv  -> asset_emissions
    (the _ownership_ and _confidence_ sibling files are skipped — different schemas)
"""

import csv
import io
import os
import tempfile
import zipfile

import pyarrow as pa
import pyarrow.csv as pacsv

from subsets_utils import (
    NodeSpec,
    SqlNodeSpec,
    get,
    get_client,
    save_raw_parquet,
    raw_parquet_writer,
    transient_retry,
)

GAS = "co2e_100yr"
COUNTRIES_URL = "https://api.climatetrace.org/v6/definitions/countries"
PKG_URL = "https://downloads.climatetrace.org/latest/country_packages/{gas}/{iso3}.zip"

# Source-level CSVs hold millions of rows across all countries, so they are
# parsed with pyarrow's C++ CSV reader (streaming batches) — orders of magnitude
# faster than per-row Python parsing, which timed out the cloud job.
ASSET_COLUMN_TYPES = {
    "source_id": pa.string(),
    "source_name": pa.string(),
    "source_type": pa.string(),
    "iso3_country": pa.string(),
    "sector": pa.string(),
    "subsector": pa.string(),
    "start_time": pa.string(),
    "end_time": pa.string(),
    "lat": pa.float64(),
    "lon": pa.float64(),
    "gas": pa.string(),
    "emissions_quantity": pa.float64(),
    "temporal_granularity": pa.string(),
    "activity": pa.float64(),
    "activity_units": pa.string(),
    "emissions_factor": pa.float64(),
    "emissions_factor_units": pa.string(),
    "capacity": pa.float64(),
    "capacity_units": pa.string(),
    "capacity_factor": pa.float64(),
}
ASSET_CONVERT = pacsv.ConvertOptions(
    include_columns=list(ASSET_COLUMN_TYPES.keys()),
    include_missing_columns=True,
    column_types=ASSET_COLUMN_TYPES,
    strings_can_be_null=True,
)
ASSET_READ = pacsv.ReadOptions(block_size=1 << 24)  # 16 MB blocks

COUNTRY_EMISSIONS_SCHEMA = pa.schema([
    ("iso3_country", pa.string()),
    ("sector", pa.string()),
    ("subsector", pa.string()),
    ("start_time", pa.string()),
    ("end_time", pa.string()),
    ("gas", pa.string()),
    ("emissions_quantity", pa.float64()),
    ("emissions_quantity_units", pa.string()),
    ("temporal_granularity", pa.string()),
    ("created_date", pa.string()),
    ("modified_date", pa.string()),
])

ASSET_EMISSIONS_SCHEMA = pa.schema([
    ("source_id", pa.string()),
    ("source_name", pa.string()),
    ("source_type", pa.string()),
    ("iso3_country", pa.string()),
    ("sector", pa.string()),
    ("subsector", pa.string()),
    ("start_time", pa.string()),
    ("end_time", pa.string()),
    ("lat", pa.float64()),
    ("lon", pa.float64()),
    ("gas", pa.string()),
    ("emissions_quantity", pa.float64()),
    ("temporal_granularity", pa.string()),
    ("activity", pa.float64()),
    ("activity_units", pa.string()),
    ("emissions_factor", pa.float64()),
    ("emissions_factor_units", pa.string()),
    ("capacity", pa.float64()),
    ("capacity_units", pa.string()),
    ("capacity_factor", pa.float64()),
])


def _f(x):
    """Parse a CSV cell to float, tolerating blanks / non-numeric."""
    if x is None:
        return None
    x = x.strip()
    if x == "" or x.lower() in ("na", "nan", "null", "none"):
        return None
    try:
        return float(x)
    except ValueError:
        return None


@transient_retry()
def _list_countries():
    resp = get(COUNTRIES_URL, timeout=(10.0, 60.0))
    resp.raise_for_status()
    return [c["alpha3"] for c in resp.json() if c.get("alpha3")]


@transient_retry()
def _download_country_zip(iso3):
    """Stream a country package to a temp file; return its path (or None on 404)."""
    url = PKG_URL.format(gas=GAS, iso3=iso3)
    tmp = tempfile.NamedTemporaryFile(suffix=".zip", delete=False)
    try:
        with get_client().stream("GET", url, timeout=(10.0, 300.0)) as resp:
            if resp.status_code == 404:
                # Permanent: this country has no package — skip it.
                resp.close()
                tmp.close()
                os.unlink(tmp.name)
                return None
            resp.raise_for_status()
            for chunk in resp.iter_bytes(1 << 20):
                tmp.write(chunk)
        tmp.close()
        return tmp.name
    except Exception:
        tmp.close()
        if os.path.exists(tmp.name):
            os.unlink(tmp.name)
        raise


def _members(zf, infix):
    """Members of the wanted CSV family, excluding ownership/confidence siblings."""
    out = []
    for n in zf.namelist():
        if not n.endswith(".csv"):
            continue
        if infix in n and "_ownership_" not in n and "_confidence_" not in n:
            out.append(n)
    return out


def fetch_country_emissions(node_id: str) -> None:
    asset = node_id  # the runtime passes the spec id; it IS the asset name
    cols = COUNTRY_EMISSIONS_SCHEMA.names
    rows = []
    countries = _list_countries()
    if not countries:
        raise AssertionError("country definitions API returned no countries")
    seen = 0
    for iso3 in countries:
        path = _download_country_zip(iso3)
        if path is None:
            continue
        try:
            with zipfile.ZipFile(path) as zf:
                for member in _members(zf, "_country_emissions_"):
                    with zf.open(member) as fh:
                        reader = csv.DictReader(io.TextIOWrapper(fh, encoding="utf-8"))
                        for r in reader:
                            rows.append({
                                **{c: (r.get(c) or None) for c in cols},
                                "emissions_quantity": _f(r.get("emissions_quantity")),
                            })
            seen += 1
        finally:
            os.unlink(path)
    if not rows:
        raise AssertionError("no country_emissions rows parsed from any package")
    table = pa.Table.from_pylist(rows, schema=COUNTRY_EMISSIONS_SCHEMA)
    print(f"  {asset}: {len(rows)} rows from {seen} country packages")
    save_raw_parquet(table, asset)


def fetch_asset_emissions(node_id: str) -> None:
    asset = node_id
    countries = _list_countries()
    if not countries:
        raise AssertionError("country definitions API returned no countries")

    names = ASSET_EMISSIONS_SCHEMA.names
    total = 0
    with raw_parquet_writer(asset, ASSET_EMISSIONS_SCHEMA) as writer:
        for iso3 in countries:
            path = _download_country_zip(iso3)
            if path is None:
                continue
            try:
                with zipfile.ZipFile(path) as zf:
                    for member in _members(zf, "_emissions_sources_"):
                        with zf.open(member) as fh:
                            reader = pacsv.open_csv(
                                fh, read_options=ASSET_READ,
                                convert_options=ASSET_CONVERT,
                            )
                            for batch in reader:
                                # reorder to the declared schema and write
                                tbl = pa.Table.from_batches([batch]).select(names)
                                writer.write_table(tbl)
                                total += tbl.num_rows
            finally:
                os.unlink(path)
    if total == 0:
        raise AssertionError("no asset_emissions rows parsed from any package")
    print(f"  {asset}: {total} source-level rows")


DOWNLOAD_SPECS = [
    NodeSpec(id="climate-trace-country-emissions", fn=fetch_country_emissions, kind="download"),
    NodeSpec(id="climate-trace-asset-emissions", fn=fetch_asset_emissions, kind="download"),
]

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="climate-trace-country-emissions-transform",
        deps=["climate-trace-country-emissions"],
        sql='''
            SELECT
                iso3_country,
                sector,
                subsector,
                gas,
                CAST(start_time AS TIMESTAMP)        AS period_start,
                CAST(end_time   AS TIMESTAMP)        AS period_end,
                CAST(substr(start_time, 1, 4) AS INTEGER) AS year,
                temporal_granularity,
                CAST(emissions_quantity AS DOUBLE)   AS emissions_quantity,
                emissions_quantity_units             AS units
            FROM "climate-trace-country-emissions"
            WHERE emissions_quantity IS NOT NULL
              AND iso3_country IS NOT NULL
            QUALIFY row_number() OVER (
                PARTITION BY iso3_country, subsector, gas, start_time, temporal_granularity
                ORDER BY modified_date DESC
            ) = 1
        ''',
    ),
    SqlNodeSpec(
        id="climate-trace-asset-emissions-transform",
        deps=["climate-trace-asset-emissions"],
        sql='''
            SELECT
                source_id,
                source_name,
                source_type,
                iso3_country,
                sector,
                subsector,
                gas,
                lat,
                lon,
                CAST(start_time AS TIMESTAMP)        AS period_start,
                CAST(end_time   AS TIMESTAMP)        AS period_end,
                CAST(substr(start_time, 1, 4) AS INTEGER) AS year,
                temporal_granularity,
                emissions_quantity,
                activity,
                activity_units,
                emissions_factor,
                emissions_factor_units,
                capacity,
                capacity_units,
                capacity_factor
            FROM "climate-trace-asset-emissions"
            WHERE emissions_quantity IS NOT NULL
              AND source_id IS NOT NULL
            QUALIFY row_number() OVER (
                PARTITION BY source_id, subsector, gas, start_time, end_time, temporal_granularity
                ORDER BY emissions_quantity DESC
            ) = 1
        ''',
    ),
]
