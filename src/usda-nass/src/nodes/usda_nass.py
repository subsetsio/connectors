"""USDA NASS Quick Stats — one long-format agricultural-statistics asset per commodity.

Source: the complete Quick Stats database, published as 5 gzipped tab-delimited
sector dumps at https://www.nass.usda.gov/datasets/. The REST API serves the same
data but is API-key gated and the deployment holds no such secret, so the bulk
files are the servable route (see research). Filenames carry a YYYYMMDD stamp that
rotates roughly weekly, so the URLs are not persistent: the directory listing is
scraped for the current stamp on every run.

Shape: stateless full re-pull. The 5 files are complete snapshots with no
since/cursor parameter, so every run re-fetches the whole corpus and overwrites.
Revisions and late corrections are therefore picked up for free.

Architecture — one bulk fetch fanning out to 434 commodity assets:
  * `load_quickstats` (the spec for entity `ag-land`) downloads each sector file
    once, streams it through DuckDB into a local parquet cache partitioned by
    COMMODITY_DESC, then writes one raw parquet asset per accepted commodity.
    Re-fetching a 1.1 GB dump once per commodity would cost ~490 GB of transfer.
  * Every other commodity spec declares the loader as a dependency and verifies
    that its slice landed. The harness requires one download spec per accepted
    entity; the work behind them is genuinely shared.

Cleaning happens here, in the fetch, so the raw is already SQL-readable and typed:
YEAR -> INTEGER, WEEK_ENDING -> DATE, LOAD_TIME -> TIMESTAMP, VALUE/CV_% -> DOUBLE.
VALUE carries thousands separators and USDA suppression codes ((D) withheld,
(Z) rounds to zero, (NA), (X), '.'); those parse to NULL and the original token is
preserved in `value_flag` so suppression stays distinguishable from absence. CV_%
uses a NUL byte as its empty marker, so NULs are stripped from every text column.

No MAINTAIN_SPECS: the bulk URL rotates weekly, so a stored ETag/Last-Modified
signature never matches the next run's URL and `source_unchanged` could not skip.
Refresh cadence is owned by maintenance.json instead.
"""

import os
import re
import shutil
import tempfile

import duckdb

from subsets_utils import (
    NodeSpec,
    get,
    get_client,
    raw_asset_exists,
    raw_parquet_writer,
    transient_retry,
)

from constants import COMMODITY_DESC, ENTITY_IDS

SLUG = "usda-nass"
INDEX_URL = "https://www.nass.usda.gov/datasets/"
SECTOR_TOKENS = ("animals_products", "crops", "demographics", "economics", "environmental")
BULK_FILE_RE = re.compile(r"qs\.[a-z_]+_\d{8}\.txt\.gz")

# The entity whose spec owns the bulk fetch. Arbitrary but fixed: every other
# spec depends on it, so it must not drift when the catalog is re-collected.
LOADER_ID = "ag-land"

# NUL (0x00) is CV_%'s empty marker; it also has no business in a published
# string column, so every passthrough text column is scrubbed.
_CLEAN = "nullif(replace({src}, chr(0), ''), '')"
# VALUE/CV_% are strings: thousands separators, parenthesized suppression codes.
_NUM = "TRY_CAST(replace(replace(trim({src}), ',', ''), chr(0), '') AS DOUBLE)"

# (sql expression over the raw TSV, raw column name). Order defines the asset's
# column order. `commodity` is the partition key and must appear here by name.
PROJECTION = (
    ('COMMODITY_DESC', "commodity"),
    (_CLEAN.format(src="SECTOR_DESC"), "sector"),
    (_CLEAN.format(src="GROUP_DESC"), "commodity_group"),
    (_CLEAN.format(src="SOURCE_DESC"), "source"),
    (_CLEAN.format(src="SHORT_DESC"), "series"),
    (_CLEAN.format(src="STATISTICCAT_DESC"), "statistic"),
    (_CLEAN.format(src="UNIT_DESC"), "unit"),
    (_CLEAN.format(src="CLASS_DESC"), "class"),
    (_CLEAN.format(src="PRODN_PRACTICE_DESC"), "production_practice"),
    (_CLEAN.format(src="UTIL_PRACTICE_DESC"), "utilization_practice"),
    (_CLEAN.format(src="DOMAIN_DESC"), "domain"),
    (_CLEAN.format(src="DOMAINCAT_DESC"), "domain_category"),
    (_CLEAN.format(src="AGG_LEVEL_DESC"), "agg_level"),
    (_CLEAN.format(src="LOCATION_DESC"), "location"),
    (_CLEAN.format(src="STATE_ALPHA"), "state_code"),
    (_CLEAN.format(src="STATE_NAME"), "state"),
    (_CLEAN.format(src="STATE_ANSI"), "state_ansi"),
    (_CLEAN.format(src="STATE_FIPS_CODE"), "state_fips_code"),
    (_CLEAN.format(src="ASD_CODE"), "asd_code"),
    (_CLEAN.format(src="ASD_DESC"), "agricultural_district"),
    (_CLEAN.format(src="COUNTY_ANSI"), "county_ansi"),
    (_CLEAN.format(src="COUNTY_CODE"), "county_code"),
    (_CLEAN.format(src="COUNTY_NAME"), "county"),
    (_CLEAN.format(src="REGION_DESC"), "region"),
    (_CLEAN.format(src="ZIP_5"), "zip_code"),
    (_CLEAN.format(src="WATERSHED_CODE"), "watershed_code"),
    (_CLEAN.format(src="WATERSHED_DESC"), "watershed"),
    (_CLEAN.format(src="CONGR_DISTRICT_CODE"), "congressional_district"),
    (_CLEAN.format(src="COUNTRY_CODE"), "country_code"),
    (_CLEAN.format(src="COUNTRY_NAME"), "country"),
    ('TRY_CAST("YEAR" AS INTEGER)', "year"),
    (_CLEAN.format(src="FREQ_DESC"), "frequency"),
    (_CLEAN.format(src="REFERENCE_PERIOD_DESC"), "reference_period"),
    (_CLEAN.format(src="BEGIN_CODE"), "begin_code"),
    (_CLEAN.format(src="END_CODE"), "end_code"),
    ("TRY_CAST(WEEK_ENDING AS DATE)", "week_ending"),
    (_NUM.format(src="VALUE"), "value"),
    (f'CASE WHEN {_NUM.format(src="VALUE")} IS NULL '
     f"THEN {_CLEAN.format(src='trim(VALUE)')} END", "value_flag"),
    (_NUM.format(src='"CV_%"'), "cv_percent"),
    ("TRY_CAST(LOAD_TIME AS TIMESTAMP)", "load_time"),
)

RAW_COLUMNS = tuple(name for _expr, name in PROJECTION)


def _read_tsv(path: str) -> str:
    """A read_csv clause over one gzipped sector dump. Every column is read as
    text (`all_varchar`) and typed by PROJECTION: NASS ships suppression codes and
    thousands separators inside otherwise-numeric columns, so letting the CSV
    sniffer guess types would either fail the scan or silently drop rows."""
    return (
        f"read_csv('{path}', delim='\t', header=true, all_varchar=true, "
        "quote='', escape='', encoding='latin-1', strict_mode=false)"
    )


def _discover_urls() -> dict[str, str]:
    """Scrape the directory listing for the current YYYYMMDD stamp and map each
    sector token to its bulk-file URL."""
    resp = get(INDEX_URL, timeout=(10.0, 120.0))
    resp.raise_for_status()
    names = sorted(set(BULK_FILE_RE.findall(resp.text)))
    urls = {
        tok: INDEX_URL + name
        for name in names
        for tok in SECTOR_TOKENS
        if name.startswith(f"qs.{tok}_")
    }
    missing = [t for t in SECTOR_TOKENS if t not in urls]
    if missing:
        raise RuntimeError(
            f"no bulk file listed for sector(s) {missing} at {INDEX_URL} "
            f"(listing matched: {names})"
        )
    return urls


@transient_retry()
def _download(url: str, dest: str) -> None:
    """Stream one sector dump to local disk — crops alone is 1.1 GB compressed,
    far past what an in-memory response can hold. `get_client().stream` bypasses
    the retry baked into `get`, so the policy is applied here."""
    with get_client().stream("GET", url, timeout=(30.0, 900.0)) as resp:
        resp.raise_for_status()
        with open(dest, "wb") as fh:
            for chunk in resp.iter_bytes(chunk_size=8 * 1024 * 1024):
                fh.write(chunk)


def _assert_casts_lossless(con: duckdb.DuckDBPyConnection, source: str, tok: str) -> None:
    """TRY_CAST turns an unparseable value into NULL, which would silently hollow
    out a column if NASS ever changed a date or year format. Count the casts that
    would lose a non-null source value and raise before any of it is written."""
    bad_year, bad_week, bad_load, bad_commodity = con.execute(
        f"""SELECT
          count(*) FILTER (WHERE "YEAR" IS NOT NULL AND TRY_CAST("YEAR" AS INTEGER) IS NULL),
          count(*) FILTER (WHERE WEEK_ENDING IS NOT NULL AND TRY_CAST(WEEK_ENDING AS DATE) IS NULL),
          count(*) FILTER (WHERE LOAD_TIME IS NOT NULL AND TRY_CAST(LOAD_TIME AS TIMESTAMP) IS NULL),
          count(*) FILTER (WHERE COMMODITY_DESC IS NULL)
        FROM {source}"""
    ).fetchone()
    problems = [
        f"{n} row(s) with unparseable {col}"
        for n, col in ((bad_year, "YEAR"), (bad_week, "WEEK_ENDING"),
                       (bad_load, "LOAD_TIME"), (bad_commodity, "COMMODITY_DESC"))
        if n
    ]
    if problems:
        raise RuntimeError(f"sector {tok}: source format changed - " + "; ".join(problems))


def load_quickstats(node_id: str) -> None:
    """LOADER: fetch all 5 sector dumps, partition them by commodity, and write one
    raw parquet asset per accepted commodity. Every other download node depends on
    this one; it is invoked as the fetch fn of the `ag-land` spec."""
    base = tempfile.mkdtemp(prefix="nass_")
    part_root = os.path.join(base, "part")
    try:
        con = duckdb.connect()
        con.execute(f"SET temp_directory='{os.path.join(base, 'duckdb_tmp')}'")
        con.execute("SET preserve_insertion_order=false")

        urls = _discover_urls()
        projection = ", ".join(f'{expr} AS "{name}"' for expr, name in PROJECTION)

        for tok in SECTOR_TOKENS:
            gz = os.path.join(base, f"{tok}.txt.gz")
            print(f"[loader] downloading {urls[tok]}", flush=True)
            _download(urls[tok], gz)
            source = _read_tsv(gz)
            _assert_casts_lossless(con, source, tok)
            print(f"[loader] partitioning {tok} by commodity", flush=True)
            # One shared partition root across sectors: a commodity that spans
            # several sectors lands in one directory, so its slice is a single
            # pruned read. FILENAME_PATTERN keeps the sectors from colliding.
            con.execute(
                f"COPY (SELECT {projection} FROM {source}) TO '{part_root}' "
                "(FORMAT PARQUET, PARTITION_BY (commodity), OVERWRITE_OR_IGNORE, "
                f"FILENAME_PATTERN '{tok}_{{i}}', COMPRESSION zstd)"
            )
            os.remove(gz)

        # `commodity` is the partition key, so it is stripped from the files and
        # restored from the directory name — hence the explicit projection and
        # the WHERE, which DuckDB turns into partition pruning.
        columns = ", ".join(f'"{c}"' for c in RAW_COLUMNS)
        glob = os.path.join(part_root, "**", "*.parquet")
        empty = []
        for entity_id in ENTITY_IDS:
            commodity = COMMODITY_DESC[entity_id].replace("'", "''")
            reader = con.execute(
                f"SELECT {columns} FROM read_parquet('{glob}', hive_partitioning=true) "
                f"WHERE commodity = '{commodity}'"
            ).fetch_record_batch()
            rows = 0
            with raw_parquet_writer(f"{SLUG}-{entity_id}", reader.schema) as writer:
                for batch in reader:
                    if batch.num_rows:
                        writer.write_batch(batch)
                        rows += batch.num_rows
            if not rows:
                empty.append(entity_id)
        if empty:
            # An accepted commodity with no rows means the corpus changed under
            # us. Fail loudly rather than publish an empty table.
            raise RuntimeError(
                f"{len(empty)} accepted commodit(ies) absent from the bulk dump: "
                f"{', '.join(sorted(empty))}"
            )
    finally:
        shutil.rmtree(base, ignore_errors=True)


def verify_commodity_slice(node_id: str) -> None:
    """Non-loader commodity node: its raw asset is written by `load_quickstats`,
    a declared dependency. Confirm the slice landed — this is a post-condition on
    the loader, not a freshness short-circuit; there is nothing left to fetch."""
    if not raw_asset_exists(node_id, "parquet"):
        raise RuntimeError(
            f"{node_id}: raw asset missing after loader '{SLUG}-{LOADER_ID}' ran"
        )


DOWNLOAD_SPECS = [
    NodeSpec(
        id=f"{SLUG}-{entity_id.lower().replace('_', '-')}",
        fn=load_quickstats if entity_id == LOADER_ID else verify_commodity_slice,
        kind="download",
        deps=() if entity_id == LOADER_ID else (f"{SLUG}-{LOADER_ID}",),
    )
    for entity_id in ENTITY_IDS
]
