"""Project FeederWatch connector.

Single citizen-science source (Cornell Lab of Ornithology + Birds Canada):
standardized bird counts at supplementary feeding stations across the US and
Canada since 1988. Access is bulk static CSV/ZIP on cdn.feederwatch.org.

Shape: stateless full re-pull. The whole corpus is a fixed set of bulk files
republished annually (~June 1); we re-fetch and overwrite every run, so late
corrections and the new season are picked up for free. No incremental filter
exists and none is needed.

URLs are point-in-time — both the path segment (e.g. 202406) and the filename
date stamp (May2024) increment each annual release — so we never hardcode them.
Each fetch fn scrapes the entry page and resolves the current links.

Three subsets:
  * observations        — the core checklist counts (7 year-range ZIPs, one
                          shared schema, streamed into one parquet).
  * site_descriptions   — per-site/per-period habitat & feeder attributes.
  * species_translation — the species codebook (code -> names + taxonomy).
"""

import io
import re
import zipfile

import pyarrow as pa
import pyarrow.csv as pacsv

from subsets_utils import (
    NodeSpec,
    SqlNodeSpec,
    get,
    configure_http,
    transient_retry,
    save_raw_parquet,
    raw_parquet_writer,
)

ENTRY_URL = "https://feederwatch.org/explore/raw-dataset-requests/"

# feederwatch.org / cdn.feederwatch.org sit behind a WAF that 403s bare clients
# from datacenter IPs. A full browser-like header set gets through. ASCII only.
_BROWSER_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
}

# Header is identical across all year-range files (verified 1988-1995,
# 2006-2010, 2021-2024). Read every column as string and let "NA"/"" be null;
# the transform does the typing. A fixed all-string schema keeps the streamed
# parquet contract stable across the 7 files and across annual releases.
OBS_COLUMNS = [
    "LOC_ID", "LATITUDE", "LONGITUDE", "SUBNATIONAL1_CODE", "ENTRY_TECHNIQUE",
    "SUB_ID", "OBS_ID", "Month", "Day", "Year", "PROJ_PERIOD_ID",
    "SPECIES_CODE", "alt_full_spp_code", "HOW_MANY", "PLUS_CODE", "VALID",
    "REVIEWED", "DAY1_AM", "DAY1_PM", "DAY2_AM", "DAY2_PM",
    "EFFORT_HRS_ATLEAST", "SNOW_DEP_ATLEAST", "Data_Entry_Method",
]
OBS_SCHEMA = pa.schema([(c, pa.string()) for c in OBS_COLUMNS])

_NULL_VALUES = ["NA", "na", "NaN", ""]


@transient_retry()
def _fetch(url: str):
    # Long read timeout: the year-range ZIPs are tens-to-hundreds of MB.
    resp = get(url, timeout=(10.0, 600.0))
    resp.raise_for_status()
    return resp


def _entry_links() -> list[str]:
    """All cdn.feederwatch.org links on the entry page (current release)."""
    html = _fetch(ENTRY_URL).text
    links = re.findall(r"https://cdn\.feederwatch\.org/data/[^\s\"'<>]+", html)
    if not links:
        raise RuntimeError(f"no cdn.feederwatch.org links found on {ENTRY_URL}")
    return links


def _resolve_one(pattern: str) -> str:
    """Return the single entry-page link matching `pattern`, else raise."""
    rx = re.compile(pattern)
    hits = sorted({u for u in _entry_links() if rx.search(u)})
    if not hits:
        raise RuntimeError(f"no entry-page link matched {pattern!r} on {ENTRY_URL}")
    if len(hits) > 1:
        raise RuntimeError(f"expected one link for {pattern!r}, got {len(hits)}: {hits}")
    return hits[0]


def _read_csv_bytes(content: bytes) -> pa.Table:
    """Parse an in-memory CSV (NA -> null), inferring column types."""
    co = pacsv.ConvertOptions(null_values=_NULL_VALUES, strings_can_be_null=True)
    return pacsv.read_csv(io.BytesIO(content), convert_options=co)


def fetch_observations(node_id: str) -> None:
    configure_http(headers=_BROWSER_HEADERS)
    asset = node_id
    rx = re.compile(r"PFW_all_\d{4}_\d{4}_.*\.csv\.zip$")
    zips = sorted({u for u in _entry_links() if rx.search(u)})
    if not zips:
        raise RuntimeError(f"no observation ZIP links found on {ENTRY_URL}")

    read_opts = pacsv.ReadOptions(block_size=16 * 1024 * 1024)
    conv_opts = pacsv.ConvertOptions(
        column_types={c: pa.string() for c in OBS_COLUMNS},
        null_values=_NULL_VALUES,
        strings_can_be_null=True,
    )
    with raw_parquet_writer(asset, OBS_SCHEMA) as writer:
        for url in zips:
            resp = _fetch(url)
            zf = zipfile.ZipFile(io.BytesIO(resp.content))
            csv_name = next(
                (n for n in zf.namelist() if n.lower().endswith(".csv")), None
            )
            if csv_name is None:
                raise RuntimeError(f"no CSV inside {url}")
            with zf.open(csv_name) as f:
                reader = pacsv.open_csv(
                    f, read_options=read_opts, convert_options=conv_opts
                )
                for batch in reader:
                    # Enforce column order so every batch matches OBS_SCHEMA.
                    writer.write_batch(batch.select(OBS_COLUMNS))


def fetch_site_descriptions(node_id: str) -> None:
    configure_http(headers=_BROWSER_HEADERS)
    asset = node_id
    url = _resolve_one(r"PFW_count_site_data.*\.csv$")
    table = _read_csv_bytes(_fetch(url).content)
    save_raw_parquet(table, asset)


def fetch_species_translation(node_id: str) -> None:
    configure_http(headers=_BROWSER_HEADERS)
    asset = node_id
    url = _resolve_one(r"PFW_spp_translation_table.*\.csv$")
    table = _read_csv_bytes(_fetch(url).content)
    save_raw_parquet(table, asset)


DOWNLOAD_SPECS = [
    NodeSpec(id="feederwatch-observations", fn=fetch_observations, kind="download"),
    NodeSpec(id="feederwatch-site-descriptions", fn=fetch_site_descriptions, kind="download"),
    NodeSpec(id="feederwatch-species-translation", fn=fetch_species_translation, kind="download"),
]


TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="feederwatch-observations-transform",
        deps=["feederwatch-observations"],
        sql='''
            SELECT
                LOC_ID                              AS loc_id,
                TRY_CAST(LATITUDE  AS DOUBLE)       AS latitude,
                TRY_CAST(LONGITUDE AS DOUBLE)       AS longitude,
                SUBNATIONAL1_CODE                   AS subnational1_code,
                ENTRY_TECHNIQUE                     AS entry_technique,
                SUB_ID                              AS sub_id,
                OBS_ID                              AS obs_id,
                TRY_CAST(Month AS INTEGER)          AS month,
                TRY_CAST(Day   AS INTEGER)          AS day,
                TRY_CAST(Year  AS INTEGER)          AS year,
                PROJ_PERIOD_ID                      AS proj_period_id,
                SPECIES_CODE                        AS species_code,
                alt_full_spp_code                   AS alt_full_spp_code,
                TRY_CAST(HOW_MANY AS INTEGER)       AS how_many,
                PLUS_CODE                           AS plus_code,
                TRY_CAST(VALID    AS INTEGER)       AS valid,
                TRY_CAST(REVIEWED AS INTEGER)       AS reviewed,
                TRY_CAST(DAY1_AM AS INTEGER)        AS day1_am,
                TRY_CAST(DAY1_PM AS INTEGER)        AS day1_pm,
                TRY_CAST(DAY2_AM AS INTEGER)        AS day2_am,
                TRY_CAST(DAY2_PM AS INTEGER)        AS day2_pm,
                TRY_CAST(EFFORT_HRS_ATLEAST AS DOUBLE) AS effort_hrs_atleast,
                TRY_CAST(SNOW_DEP_ATLEAST   AS DOUBLE) AS snow_dep_atleast,
                Data_Entry_Method                   AS data_entry_method
            FROM "feederwatch-observations"
            WHERE OBS_ID IS NOT NULL
        ''',
    ),
    SqlNodeSpec(
        id="feederwatch-site-descriptions-transform",
        deps=["feederwatch-site-descriptions"],
        sql='''
            SELECT *
            FROM "feederwatch-site-descriptions"
            WHERE loc_id IS NOT NULL
        ''',
    ),
    SqlNodeSpec(
        id="feederwatch-species-translation-transform",
        deps=["feederwatch-species-translation"],
        sql='''
            SELECT
                species_code,
                alt_full_spp_code,
                TRY_CAST(n_locations AS INTEGER)          AS n_locations,
                scientific_name,
                american_english_name,
                TRY_CAST(taxonomy_version AS INTEGER)     AS taxonomy_version,
                TRY_CAST(taxonomic_sort_order AS DOUBLE)  AS taxonomic_sort_order
            FROM "feederwatch-species-translation"
            WHERE species_code IS NOT NULL
        ''',
    ),
]
