"""Fluctuations of Glaciers (FoG) database — one DOI-stamped zip per (~annual)
release containing a frictionless datapackage plus a `data/` folder of relational
CSV tables (glacier, mass_balance, change, front_variation, state, event, ...).
One published subset per table.

Fetch shape: stateless full re-pull. Each refresh resolves the *current* release
URL from the listing page (the zip filename embeds the release date, which bumps
annually) and re-downloads in full. FoG `change.csv` is ~815 MB uncompressed
(~1.1M rows) so members stream rather than materialize in memory. Tables are
written as all-VARCHAR parquet (the SQL transform owns typing) to sidestep CSV
type-inference surprises on sparse columns.
"""

from __future__ import annotations

import csv
import io
import re
import zipfile

import pyarrow as pa

from subsets_utils import NodeSpec, SqlNodeSpec, raw_parquet_writer
from utils import get_bytes, latest_url

FOG_VERSIONS_URL = "https://wgms.ch/data_databaseversions/"

# Zip filename embeds the release date; format is YYYY-MM, YYYY-MMx (letter
# suffix), or YYYY-MM-DD. max() over the matched URLs picks the newest.
_FOG_ZIP_RE = re.compile(
    r"https://wgms\.ch/downloads/DOI-WGMS-FoG-\d{4}-\d{2}(?:-\d{2}|[a-z])?\.zip"
)

_CSV_BATCH_ROWS = 50_000


def _stream_member_to_parquet(zf: zipfile.ZipFile, member: str, asset: str) -> None:
    """Stream one CSV member of the FoG zip into all-VARCHAR parquet.

    All columns are typed string; the SQL transform casts. This keeps memory
    bounded (change.csv is ~815 MB uncompressed) and avoids CSV type-inference
    failures on columns that are sparse in the first sample rows.
    """
    with zf.open(member) as fh:
        text = io.TextIOWrapper(fh, encoding="utf-8", newline="")
        reader = csv.reader(text)
        header = next(reader)
        ncol = len(header)
        schema = pa.schema([(c, pa.string()) for c in header])
        rows: list[list[str]] = []

        def _flush(writer) -> None:
            cols: list[list] = [[None] * len(rows) for _ in range(ncol)]
            for ri, r in enumerate(rows):
                for ci in range(ncol):
                    if ci < len(r):
                        v = r[ci]
                        cols[ci][ri] = v if v != "" else None
            arrays = [pa.array(c, type=pa.string()) for c in cols]
            writer.write_batch(pa.RecordBatch.from_arrays(arrays, schema=schema))

        with raw_parquet_writer(asset, schema) as writer:
            for r in reader:
                rows.append(r)
                if len(rows) >= _CSV_BATCH_ROWS:
                    _flush(writer)
                    rows = []
            if rows:
                _flush(writer)


def fetch_fog_table(node_id: str) -> None:
    asset = node_id  # the spec id IS the asset name
    table = node_id[len("wgms-fog-"):].replace("-", "_")
    member = f"data/{table}.csv"
    url = _latest_fog_url()
    print(f"  FoG: downloading {url} for member {member}")
    zf = zipfile.ZipFile(io.BytesIO(get_bytes(url)))
    if member not in zf.namelist():
        raise AssertionError(f"{member} not in FoG zip {url}; have {zf.namelist()[:20]}")
    _stream_member_to_parquet(zf, member, asset)


def _latest_fog_url() -> str:
    return latest_url(FOG_VERSIONS_URL, _FOG_ZIP_RE)


_FOG_TABLES = [
    "change", "change_band", "event", "front_variation", "glacier",
    "mass_balance", "mass_balance_band", "mass_balance_point", "state",
    "state_band",
]

DOWNLOAD_SPECS: list[NodeSpec] = [
    NodeSpec(id=f"wgms-fog-{t.replace('_', '-')}", fn=fetch_fog_table, kind="download")
    for t in _FOG_TABLES
]

TRANSFORM_SPECS: list[SqlNodeSpec] = [
    SqlNodeSpec(
        id="wgms-fog-glacier-transform",
        deps=["wgms-fog-glacier"],
        sql='''
            SELECT
                country,
                short_name,
                names,
                TRY_CAST(id AS BIGINT)                AS glacier_id,
                TRY_CAST(latitude AS DOUBLE)          AS latitude,
                TRY_CAST(longitude AS DOUBLE)         AS longitude,
                gtng_region,
                glims_id, rgi50_ids, rgi60_ids, rgi70_ids, wgi_id,
                TRY_CAST(parent_glacier_id AS BIGINT) AS parent_glacier_id,
                "references"                          AS reference_ids,
                remarks
            FROM "wgms-fog-glacier"
        ''',
    ),
    SqlNodeSpec(
        id="wgms-fog-mass-balance-transform",
        deps=["wgms-fog-mass-balance"],
        sql='''
            SELECT
                country, glacier_name,
                TRY_CAST(glacier_id AS BIGINT)            AS glacier_id,
                outline_id,
                TRY_CAST(year AS INTEGER)                 AS year,
                time_system,
                TRY_CAST(begin_date AS DATE)              AS begin_date,
                begin_date_unc,
                TRY_CAST(midseason_date AS DATE)          AS midseason_date,
                midseason_date_unc,
                TRY_CAST(end_date AS DATE)                AS end_date,
                end_date_unc,
                TRY_CAST(winter_balance AS DOUBLE)        AS winter_balance,
                TRY_CAST(winter_balance_unc AS DOUBLE)    AS winter_balance_unc,
                TRY_CAST(summer_balance AS DOUBLE)        AS summer_balance,
                TRY_CAST(summer_balance_unc AS DOUBLE)    AS summer_balance_unc,
                TRY_CAST(annual_balance AS DOUBLE)        AS annual_balance,
                TRY_CAST(annual_balance_unc AS DOUBLE)    AS annual_balance_unc,
                ela_position,
                TRY_CAST(ela AS DOUBLE)                   AS ela,
                TRY_CAST(ela_unc AS DOUBLE)               AS ela_unc,
                TRY_CAST(aar AS DOUBLE)                   AS aar,
                TRY_CAST(area AS DOUBLE)                  AS area,
                investigators, agencies, "references" AS reference_ids, remarks
            FROM "wgms-fog-mass-balance"
        ''',
    ),
    SqlNodeSpec(
        id="wgms-fog-mass-balance-band-transform",
        deps=["wgms-fog-mass-balance-band"],
        sql='''
            SELECT
                country, glacier_name,
                TRY_CAST(glacier_id AS BIGINT)         AS glacier_id,
                TRY_CAST(year AS INTEGER)              AS year,
                TRY_CAST(lower_elevation AS DOUBLE)    AS lower_elevation,
                TRY_CAST(upper_elevation AS DOUBLE)    AS upper_elevation,
                TRY_CAST(area AS DOUBLE)               AS area,
                TRY_CAST(winter_balance AS DOUBLE)     AS winter_balance,
                TRY_CAST(winter_balance_unc AS DOUBLE) AS winter_balance_unc,
                TRY_CAST(summer_balance AS DOUBLE)     AS summer_balance,
                TRY_CAST(summer_balance_unc AS DOUBLE) AS summer_balance_unc,
                TRY_CAST(annual_balance AS DOUBLE)     AS annual_balance,
                TRY_CAST(annual_balance_unc AS DOUBLE) AS annual_balance_unc,
                remarks
            FROM "wgms-fog-mass-balance-band"
        ''',
    ),
    SqlNodeSpec(
        id="wgms-fog-mass-balance-point-transform",
        deps=["wgms-fog-mass-balance-point"],
        sql='''
            SELECT
                country, glacier_name,
                TRY_CAST(glacier_id AS BIGINT)   AS glacier_id,
                TRY_CAST(year AS INTEGER)        AS year,
                TRY_CAST(id AS BIGINT)           AS id,
                original_id, time_system,
                TRY_CAST(begin_date AS DATE)     AS begin_date,
                begin_date_unc,
                TRY_CAST(end_date AS DATE)       AS end_date,
                end_date_unc,
                TRY_CAST(latitude AS DOUBLE)     AS latitude,
                TRY_CAST(longitude AS DOUBLE)    AS longitude,
                TRY_CAST(elevation AS DOUBLE)    AS elevation,
                TRY_CAST(balance AS DOUBLE)      AS balance,
                TRY_CAST(balance_unc AS DOUBLE)  AS balance_unc,
                TRY_CAST(density AS DOUBLE)      AS density,
                TRY_CAST(density_unc AS DOUBLE)  AS density_unc,
                method, balance_code, remarks
            FROM "wgms-fog-mass-balance-point"
        ''',
    ),
    SqlNodeSpec(
        id="wgms-fog-change-transform",
        deps=["wgms-fog-change"],
        sql='''
            SELECT
                country, glacier_name,
                TRY_CAST(glacier_id AS BIGINT)             AS glacier_id,
                begin_outline_id, end_outline_id,
                TRY_CAST(id AS BIGINT)                     AS id,
                TRY_CAST(begin_date AS DATE)               AS begin_date,
                begin_date_unc,
                TRY_CAST(end_date AS DATE)                 AS end_date,
                end_date_unc,
                TRY_CAST(area AS DOUBLE)                   AS area,
                TRY_CAST(elevation_change AS DOUBLE)       AS elevation_change,
                TRY_CAST(elevation_change_unc AS DOUBLE)   AS elevation_change_unc,
                TRY_CAST(volume_change AS DOUBLE)          AS volume_change,
                TRY_CAST(volume_change_unc AS DOUBLE)      AS volume_change_unc,
                begin_platform, begin_method, end_platform, end_method,
                investigators, agencies, "references" AS reference_ids, remarks
            FROM "wgms-fog-change"
        ''',
    ),
    SqlNodeSpec(
        id="wgms-fog-change-band-transform",
        deps=["wgms-fog-change-band"],
        sql='''
            SELECT
                country, glacier_name,
                TRY_CAST(glacier_id AS BIGINT)           AS glacier_id,
                TRY_CAST(change_id AS BIGINT)            AS change_id,
                TRY_CAST(lower_elevation AS DOUBLE)      AS lower_elevation,
                TRY_CAST(upper_elevation AS DOUBLE)      AS upper_elevation,
                TRY_CAST(area AS DOUBLE)                 AS area,
                TRY_CAST(elevation_change AS DOUBLE)     AS elevation_change,
                TRY_CAST(elevation_change_unc AS DOUBLE) AS elevation_change_unc,
                TRY_CAST(volume_change AS DOUBLE)        AS volume_change,
                TRY_CAST(volume_change_unc AS DOUBLE)    AS volume_change_unc,
                remarks
            FROM "wgms-fog-change-band"
        ''',
    ),
    SqlNodeSpec(
        id="wgms-fog-front-variation-transform",
        deps=["wgms-fog-front-variation"],
        sql='''
            SELECT
                country, glacier_name,
                TRY_CAST(glacier_id AS BIGINT)         AS glacier_id,
                TRY_CAST(series_id AS BIGINT)          AS series_id,
                TRY_CAST(begin_date AS DATE)           AS begin_date,
                begin_date_unc,
                TRY_CAST(end_date AS DATE)             AS end_date,
                end_date_unc,
                TRY_CAST(length_change AS DOUBLE)      AS length_change,
                TRY_CAST(length_change_unc AS DOUBLE)  AS length_change_unc,
                length_change_direction,
                end_platform, end_method,
                investigators, agencies, "references" AS reference_ids, remarks
            FROM "wgms-fog-front-variation"
        ''',
    ),
    SqlNodeSpec(
        id="wgms-fog-state-transform",
        deps=["wgms-fog-state"],
        sql='''
            SELECT
                country, glacier_name,
                TRY_CAST(glacier_id AS BIGINT)        AS glacier_id,
                outline_id,
                TRY_CAST(id AS BIGINT)                AS id,
                TRY_CAST(date AS DATE)                AS date,
                date_unc,
                TRY_CAST(highest_elevation AS DOUBLE) AS highest_elevation,
                TRY_CAST(lowest_elevation AS DOUBLE)  AS lowest_elevation,
                TRY_CAST(mean_elevation AS DOUBLE)    AS mean_elevation,
                TRY_CAST(elevation_unc AS DOUBLE)     AS elevation_unc,
                TRY_CAST(area AS DOUBLE)              AS area,
                TRY_CAST(area_unc AS DOUBLE)          AS area_unc,
                TRY_CAST(length AS DOUBLE)            AS length,
                TRY_CAST(length_unc AS DOUBLE)        AS length_unc,
                terminus_type, platform, method,
                investigators, agencies, "references" AS reference_ids, remarks
            FROM "wgms-fog-state"
        ''',
    ),
    SqlNodeSpec(
        id="wgms-fog-state-band-transform",
        deps=["wgms-fog-state-band"],
        sql='''
            SELECT
                country, glacier_name,
                TRY_CAST(glacier_id AS BIGINT)      AS glacier_id,
                TRY_CAST(state_id AS BIGINT)        AS state_id,
                TRY_CAST(lower_elevation AS DOUBLE) AS lower_elevation,
                TRY_CAST(upper_elevation AS DOUBLE) AS upper_elevation,
                TRY_CAST(mean_elevation AS DOUBLE)  AS mean_elevation,
                TRY_CAST(elevation_unc AS DOUBLE)   AS elevation_unc,
                TRY_CAST(area AS DOUBLE)            AS area,
                TRY_CAST(area_unc AS DOUBLE)        AS area_unc,
                remarks
            FROM "wgms-fog-state-band"
        ''',
    ),
    SqlNodeSpec(
        id="wgms-fog-event-transform",
        deps=["wgms-fog-event"],
        sql='''
            SELECT
                country, glacier_name,
                TRY_CAST(glacier_id AS BIGINT) AS glacier_id,
                TRY_CAST(id AS BIGINT)         AS id,
                TRY_CAST(date AS DATE)         AS date,
                date_unc,
                TRY_CAST(latitude AS DOUBLE)   AS latitude,
                TRY_CAST(longitude AS DOUBLE)  AS longitude,
                description,
                surge, calving, flood, avalanche, rockfall, debris_flow,
                earthquake, volcanic_eruption, other,
                investigators, agencies, "references" AS reference_ids, remarks
            FROM "wgms-fog-event"
        ''',
    ),
]
