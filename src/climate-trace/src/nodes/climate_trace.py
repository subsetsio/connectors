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
  - <subsector>_country_emissions_v*.csv             -> country_emissions
  - <subsector>_emissions_sources_v*.csv             -> asset_emissions
  - <subsector>_emissions_sources_confidence_v*.csv  -> asset_emissions_confidence
    (the _ownership_ siblings are skipped — different schema)

asset_emissions reduction: the source-level CSVs are published at MONTHLY grain
(~114M rows globally). That is far too granular for a single published table and
is unwieldy downstream, so the fetch aggregates each source's monthly rows to an
ANNUAL grain per (source, year) — summing emissions/activity, carrying the
constant descriptors (location, names, units) and the max reported capacity.
This is done with pyarrow's C++ hash group-by (one pass per zip member; sources
never span members) and cuts the corpus ~12x to ~10M rows.
"""

import csv
import io
import os
import tempfile
import zipfile

import pyarrow as pa
import pyarrow.csv as pacsv
import pyarrow.compute as pc

from subsets_utils import (
    NodeSpec,
    get,
    get_client,
    save_raw_parquet,
    raw_parquet_writer,
    transient_retry,
)

GAS = "co2e_100yr"
COUNTRIES_URL = "https://api.climatetrace.org/v6/definitions/countries"
DEFINITIONS_URL = "https://api.climatetrace.org/v6/definitions/{name}"
PKG_URL = "https://downloads.climatetrace.org/latest/country_packages/{gas}/{iso3}.zip"

# Source-level CSVs hold millions of rows across all countries, so they are
# parsed with pyarrow's C++ CSV reader (streaming batches) — orders of magnitude
# faster than per-row Python parsing, which timed out the cloud job.
# Columns parsed from the source-level CSV (the rest — end_time,
# temporal_granularity, emissions_factor*, capacity_factor, other1..10 — are
# dropped: they don't survive annual aggregation cleanly).
ASSET_COLUMN_TYPES = {
    "source_id": pa.string(),
    "source_name": pa.string(),
    "source_type": pa.string(),
    "iso3_country": pa.string(),
    "sector": pa.string(),
    "subsector": pa.string(),
    "gas": pa.string(),
    "start_time": pa.string(),
    "lat": pa.float64(),
    "lon": pa.float64(),
    "emissions_quantity": pa.float64(),
    "activity": pa.float64(),
    "activity_units": pa.string(),
    "capacity": pa.float64(),
    "capacity_units": pa.string(),
}
ASSET_CONVERT = pacsv.ConvertOptions(
    include_columns=list(ASSET_COLUMN_TYPES.keys()),
    include_missing_columns=True,
    column_types=ASSET_COLUMN_TYPES,
    strings_can_be_null=True,
)
ASSET_READ = pacsv.ReadOptions(block_size=1 << 24)  # 16 MB blocks

# (aggregation function, source column) -> output column. Descriptors are
# constant per source so "min" just carries the value; emissions/activity sum;
# capacity is a stock so take the max reported.
ASSET_AGG = [
    ("source_name", "min"), ("source_type", "min"), ("iso3_country", "min"),
    ("sector", "min"), ("subsector", "min"), ("gas", "min"),
    ("lat", "min"), ("lon", "min"),
    ("emissions_quantity", "sum"), ("activity", "sum"),
    ("activity_units", "min"), ("capacity", "max"), ("capacity_units", "min"),
]

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

# Annual-aggregated source-level schema (one row per source x year).
ASSET_EMISSIONS_SCHEMA = pa.schema([
    ("source_id", pa.string()),
    ("source_name", pa.string()),
    ("source_type", pa.string()),
    ("iso3_country", pa.string()),
    ("sector", pa.string()),
    ("subsector", pa.string()),
    ("gas", pa.string()),
    ("year", pa.int32()),
    ("lat", pa.float64()),
    ("lon", pa.float64()),
    ("emissions_quantity", pa.float64()),
    ("activity", pa.float64()),
    ("activity_units", pa.string()),
    ("capacity", pa.float64()),
    ("capacity_units", pa.string()),
])

CONFIDENCE_COLUMN_TYPES = {
    "source_id": pa.string(),
    "source_name": pa.string(),
    "iso3_country": pa.string(),
    "sector": pa.string(),
    "subsector": pa.string(),
    "gas": pa.string(),
    "start_time": pa.string(),
    "source_type": pa.string(),
    "capacity": pa.string(),
    "capacity_factor": pa.string(),
    "activity": pa.string(),
    "emissions_factor": pa.string(),
    "emissions_quantity": pa.string(),
}
CONFIDENCE_CONVERT = pacsv.ConvertOptions(
    include_columns=list(CONFIDENCE_COLUMN_TYPES.keys()),
    include_missing_columns=True,
    column_types=CONFIDENCE_COLUMN_TYPES,
    strings_can_be_null=True,
)
CONFIDENCE_AGG = [
    ("source_name", "min"), ("iso3_country", "min"), ("sector", "min"),
    ("subsector", "min"), ("gas", "min"), ("source_type", "min"),
    ("capacity", "min"), ("capacity_factor", "min"), ("activity", "min"),
    ("emissions_factor", "min"), ("emissions_quantity", "min"),
]

# Confidence cells are a 5-level ordinal, ascending. Aggregating them as strings
# would order them alphabetically ("high" < "low"), so the ordinal columns are
# encoded to their rank here, min-aggregated (the annual value is the LOWEST
# monthly confidence — ~4% of source-years disagree across months), and decoded
# back on the way out.
CONFIDENCE_LEVELS = pa.array(
    ["very low", "low", "medium", "high", "very high"], pa.string()
)
CONFIDENCE_ORDINAL_COLUMNS = [
    "source_type", "capacity", "capacity_factor",
    "activity", "emissions_factor", "emissions_quantity",
]

ASSET_CONFIDENCE_SCHEMA = pa.schema([
    ("source_id", pa.string()),
    ("source_name", pa.string()),
    ("iso3_country", pa.string()),
    ("sector", pa.string()),
    ("subsector", pa.string()),
    ("gas", pa.string()),
    ("year", pa.int32()),
    ("source_type_confidence", pa.string()),
    ("capacity_confidence", pa.string()),
    ("capacity_factor_confidence", pa.string()),
    ("activity_confidence", pa.string()),
    ("emissions_factor_confidence", pa.string()),
    ("emissions_quantity_confidence", pa.string()),
])

CONTINENTS_SCHEMA = pa.schema([
    ("continent", pa.string()),
])
COUNTRIES_SCHEMA = pa.schema([
    ("alpha3", pa.string()),
    ("alpha2", pa.string()),
    ("name", pa.string()),
    ("continent", pa.string()),
])
GASES_SCHEMA = pa.schema([
    ("gas", pa.string()),
])
SECTORS_SCHEMA = pa.schema([
    ("sector", pa.string()),
])
SUBSECTORS_SCHEMA = pa.schema([
    ("subsector", pa.string()),
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
def _get_definition(name):
    resp = get(DEFINITIONS_URL.format(name=name), timeout=(10.0, 60.0))
    resp.raise_for_status()
    return resp.json()


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


def _members(zf, infix, *, confidence=False):
    """Members of the wanted CSV family.

    `_emissions_sources_` is a prefix of `_emissions_sources_confidence_`, so the
    two families have to be separated explicitly rather than by infix alone.
    `_ownership_` siblings carry a different schema and are never wanted.
    """
    out = []
    for n in zf.namelist():
        if not n.endswith(".csv") or infix not in n or "_ownership_" in n:
            continue
        if ("_confidence_" in n) != confidence:
            continue
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


def _aggregate_member_to_annual(table: pa.Table) -> pa.Table:
    """Collapse a member's monthly source rows to one row per (source_id, year)."""
    year = pc.cast(pc.utf8_slice_codeunits(table.column("start_time"), 0, 4),
                   pa.int32())
    table = table.drop_columns(["start_time"]).append_column("year", year)
    grouped = table.group_by(["source_id", "year"]).aggregate(ASSET_AGG)
    # aggregate() names outputs "<col>_<func>"; rename back and reorder to schema.
    rename = {f"{col}_{fn}": col for col, fn in ASSET_AGG}
    grouped = grouped.rename_columns(
        [rename.get(n, n) for n in grouped.column_names]
    )
    return grouped.select(ASSET_EMISSIONS_SCHEMA.names).cast(ASSET_EMISSIONS_SCHEMA)


def _encode_confidence(table: pa.Table) -> pa.Table:
    """Replace each ordinal confidence column with its 0-based level rank."""
    for col in CONFIDENCE_ORDINAL_COLUMNS:
        values = table.column(col)
        ranks = pc.index_in(values, value_set=CONFIDENCE_LEVELS)
        unmapped = pc.sum(pc.and_(pc.is_valid(values), pc.is_null(ranks))).as_py()
        if unmapped:
            raise AssertionError(
                f"{unmapped} {col} cell(s) outside the known confidence levels"
            )
        table = table.set_column(table.schema.get_field_index(col), col, ranks)
    return table


def _aggregate_confidence_to_annual(table: pa.Table) -> pa.Table:
    year = pc.cast(pc.utf8_slice_codeunits(table.column("start_time"), 0, 4),
                   pa.int32())
    table = table.drop_columns(["start_time"]).append_column("year", year)
    table = _encode_confidence(table)
    grouped = table.group_by(["source_id", "year"]).aggregate(CONFIDENCE_AGG)
    rename = {
        "source_name_min": "source_name",
        "iso3_country_min": "iso3_country",
        "sector_min": "sector",
        "subsector_min": "subsector",
        "gas_min": "gas",
        "source_type_min": "source_type_confidence",
        "capacity_min": "capacity_confidence",
        "capacity_factor_min": "capacity_factor_confidence",
        "activity_min": "activity_confidence",
        "emissions_factor_min": "emissions_factor_confidence",
        "emissions_quantity_min": "emissions_quantity_confidence",
    }
    grouped = grouped.rename_columns(
        [rename.get(n, n) for n in grouped.column_names]
    )
    for col in CONFIDENCE_ORDINAL_COLUMNS:
        out = rename[f"{col}_min"]
        idx = grouped.schema.get_field_index(out)
        decoded = pc.take(CONFIDENCE_LEVELS, grouped.column(out))
        grouped = grouped.set_column(idx, out, decoded)
    return grouped.select(ASSET_CONFIDENCE_SCHEMA.names).cast(ASSET_CONFIDENCE_SCHEMA)


def fetch_asset_emissions(node_id: str) -> None:
    asset = node_id
    countries = _list_countries()
    if not countries:
        raise AssertionError("country definitions API returned no countries")

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
                            tbl = pacsv.read_csv(
                                fh, read_options=ASSET_READ,
                                convert_options=ASSET_CONVERT,
                            )
                        if tbl.num_rows == 0:
                            continue
                        annual = _aggregate_member_to_annual(tbl)
                        writer.write_table(annual)
                        total += annual.num_rows
            finally:
                os.unlink(path)
    if total == 0:
        raise AssertionError("no asset_emissions rows parsed from any package")
    print(f"  {asset}: {total} annual source-level rows")


def fetch_asset_confidence(node_id: str) -> None:
    asset = node_id
    countries = _list_countries()
    if not countries:
        raise AssertionError("country definitions API returned no countries")

    total = 0
    with raw_parquet_writer(asset, ASSET_CONFIDENCE_SCHEMA) as writer:
        for iso3 in countries:
            path = _download_country_zip(iso3)
            if path is None:
                continue
            try:
                with zipfile.ZipFile(path) as zf:
                    for member in _members(zf, "_emissions_sources_", confidence=True):
                        with zf.open(member) as fh:
                            tbl = pacsv.read_csv(
                                fh, read_options=ASSET_READ,
                                convert_options=CONFIDENCE_CONVERT,
                            )
                        if tbl.num_rows == 0:
                            continue
                        annual = _aggregate_confidence_to_annual(tbl)
                        writer.write_table(annual)
                        total += annual.num_rows
            finally:
                os.unlink(path)
    if total == 0:
        raise AssertionError("no confidence rows parsed from any package")
    print(f"  {asset}: {total} annual confidence rows")


def fetch_continents(node_id: str) -> None:
    rows = [{"continent": v} for v in _get_definition("continents")]
    save_raw_parquet(pa.Table.from_pylist(rows, schema=CONTINENTS_SCHEMA), node_id)


def fetch_countries(node_id: str) -> None:
    rows = _get_definition("countries")
    save_raw_parquet(pa.Table.from_pylist(rows, schema=COUNTRIES_SCHEMA), node_id)


def fetch_gases(node_id: str) -> None:
    rows = [{"gas": v} for v in _get_definition("gases")]
    save_raw_parquet(pa.Table.from_pylist(rows, schema=GASES_SCHEMA), node_id)


def fetch_sectors(node_id: str) -> None:
    rows = [{"sector": v} for v in _get_definition("sectors")]
    save_raw_parquet(pa.Table.from_pylist(rows, schema=SECTORS_SCHEMA), node_id)


def fetch_subsectors(node_id: str) -> None:
    rows = [{"subsector": v} for v in _get_definition("subsectors")]
    save_raw_parquet(pa.Table.from_pylist(rows, schema=SUBSECTORS_SCHEMA), node_id)


DOWNLOAD_SPECS = [
    NodeSpec(id="climate-trace-country-emissions", fn=fetch_country_emissions, kind="download"),
    NodeSpec(id="climate-trace-asset-emissions", fn=fetch_asset_emissions, kind="download"),
    NodeSpec(id="climate-trace-asset-emissions-confidence", fn=fetch_asset_confidence, kind="download"),
    NodeSpec(id="climate-trace-continents", fn=fetch_continents, kind="download"),
    NodeSpec(id="climate-trace-countries", fn=fetch_countries, kind="download"),
    NodeSpec(id="climate-trace-gases", fn=fetch_gases, kind="download"),
    NodeSpec(id="climate-trace-sectors", fn=fetch_sectors, kind="download"),
    NodeSpec(id="climate-trace-subsectors", fn=fetch_subsectors, kind="download"),
]
