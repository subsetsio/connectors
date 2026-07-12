"""UNEP — SDG 6.6.1 Freshwater Ecosystems (surface-water extent).

UNEP is the custodian agency for SDG indicator 6.6.1. This connector publishes
the aggregate time-series statistics behind the UNEP Freshwater Ecosystems
Explorer (map.sdg661.app), served as static CSVs from the public Google Cloud
Storage bucket `global-surface-water-stats` (research mechanism `freshwater_gcs`).

Each CSV is annual surface-water-extent statistics (permanent / seasonal area in
km2, plus projected and 5-year-smoothed variants), 1984-2018, keyed by a spatial
unit. Four publishable tables, one per spatial-aggregation level:

  unep-national          gaul0-all-2018.csv        country (GAUL ADM0)
  unep-subnational-adm1  gaul1-all-2018.csv        first-level admin region
  unep-subnational-adm2  gaul2-all-2018.csv        second-level admin region
  unep-basins            hydrobasins{3,4,5,6}-...   HydroBASINS Pfafstetter basins

The four HydroBASINS files (Pfafstetter levels 3-6) share one schema and unite
into the single `basins` table, with the Pfafstetter level carried as an explicit
`level` column (verified: hbN files contain exactly N-digit PFAF_IDs).

The CSVs are parsed at download time with pyarrow.csv into typed parquet — this
is the parse step that handles RFC-4180 quoting correctly (admin names like
"Moldova, Republic of" contain embedded commas) and pins column types, rather
than leaving DuckDB to auto-detect quoting/types over a 20k-row sample.

Fetch shape: stateless full re-pull. The whole corpus is a handful of static
CSVs (~270 MB total, gaul2 being 186 MB) re-fetched and overwritten each run;
the source publishes re-versioned filenames (e.g. a future `-2024`) rather than
updating in place, and there is no incremental/delta filter (per research). No
auth, no documented or observed rate limit (public GCS).
"""

import io

import pyarrow as pa
import pyarrow.csv as pacsv

from subsets_utils import (
    NodeSpec,
    get,
    save_raw_parquet,
    transient_retry,
)

_BUCKET = "https://storage.googleapis.com/global-surface-water-stats"

# The six surface-water metric columns are shared by every level (km2 area).
# Source header -> published name. projected* are the methodology's projected
# variants; *_5yr the 5-year smoothed series.
_METRIC_RENAME = {
    "permanent": "permanent_sq_km",
    "projectedPermanent": "projected_permanent_sq_km",
    "5yr_Permanent": "permanent_5yr_sq_km",
    "seasonal": "seasonal_sq_km",
    "projectedSeasonal": "projected_seasonal_sq_km",
    "5yr_Seasonal": "seasonal_5yr_sq_km",
}
_METRIC_TYPES = {src: pa.float64() for src in _METRIC_RENAME}

# Per-spec fetch plan. `files` is a list of (filename, level); level is None for
# admin levels and the HydroBASINS Pfafstetter level (3-6) for basins. `types`
# pins the non-metric column types; `rename` maps source header -> published
# name (and selects/orders the columns we keep). Metric columns are appended
# from the shared maps above.
_ENTITIES = {
    "unep-national": {
        "files": [("gaul0-all-2018.csv", None)],
        "types": {"year": pa.int64(), "ADM0_NAME": pa.string(), "ADM0_CODE": pa.int64()},
        "rename": {"year": "year", "ADM0_CODE": "adm0_code", "ADM0_NAME": "country_name"},
    },
    "unep-subnational-adm1": {
        "files": [("gaul1-all-2018.csv", None)],
        "types": {
            "year": pa.int64(),
            "ADM0_NAME": pa.string(), "ADM1_NAME": pa.string(),
            "ADM0_CODE": pa.int64(), "ADM1_CODE": pa.int64(),
        },
        "rename": {
            "year": "year",
            "ADM0_CODE": "adm0_code", "ADM0_NAME": "country_name",
            "ADM1_CODE": "adm1_code", "ADM1_NAME": "region_name",
        },
    },
    "unep-subnational-adm2": {
        "files": [("gaul2-all-2018.csv", None)],
        "types": {
            "year": pa.int64(),
            "ADM0_NAME": pa.string(), "ADM1_NAME": pa.string(), "ADM2_NAME": pa.string(),
            "ADM0_CODE": pa.int64(), "ADM1_CODE": pa.int64(), "ADM2_CODE": pa.int64(),
        },
        "rename": {
            "year": "year",
            "ADM0_CODE": "adm0_code", "ADM0_NAME": "country_name",
            "ADM1_CODE": "adm1_code", "ADM1_NAME": "region_name",
            "ADM2_CODE": "adm2_code", "ADM2_NAME": "district_name",
        },
    },
    "unep-basins": {
        "files": [(f"hydrobasins{lvl}-all-2018.csv", lvl) for lvl in (3, 4, 5, 6)],
        "types": {"year": pa.int64(), "PFAF_ID": pa.int64()},
        "rename": {"year": "year", "PFAF_ID": "pfaf_id"},
    },
}


@transient_retry()
def _download_csv(filename: str) -> bytes:
    # GCS serves the full table in one GET; read timeout is generous for the
    # 186 MB gaul2 file. raise_for_status() inside the retried fn so 5xx/429
    # are classified as transient and retried.
    resp = get(f"{_BUCKET}/{filename}", timeout=(10.0, 300.0))
    resp.raise_for_status()
    return resp.content


def fetch_one(node_id: str) -> None:
    """Fetch the source CSV(s) for one spec and save them as typed parquet.

    The runtime passes the spec id; it is also the asset name. pyarrow.csv parses
    with correct quoting and the pinned column_types below. basins fetches four
    HydroBASINS CSVs and unions them, carrying the Pfafstetter level explicitly.
    """
    asset = node_id
    cfg = _ENTITIES[node_id]
    convert_types = {**cfg["types"], **_METRIC_TYPES}
    rename = {**cfg["rename"], **_METRIC_RENAME}
    out_names = list(rename.values())

    tables = []
    for filename, level in cfg["files"]:
        content = _download_csv(filename)
        table = pacsv.read_csv(
            io.BytesIO(content),
            convert_options=pacsv.ConvertOptions(column_types=convert_types),
        )
        # Select the known source columns (drops any extras, fixes order) and
        # rename to the published names.
        table = table.select(list(rename.keys())).rename_columns(out_names)
        if level is not None:
            table = table.append_column(
                "level", pa.array([level] * table.num_rows, type=pa.int32())
            )
        tables.append(table)

    save_raw_parquet(pa.concat_tables(tables), asset)


DOWNLOAD_SPECS = [
    NodeSpec(id=spec_id, fn=fetch_one, kind="download") for spec_id in _ENTITIES
]
