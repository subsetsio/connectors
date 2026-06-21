"""Annual Mass-Change Estimates (AMCE) — per GTN-G region.

All per-region CSVs share one schema; region (the filename stem) becomes a
column. Small (~21 regions x ~100 years), so build in memory as ndjson.
"""

from __future__ import annotations

import csv
import io
import re
import zipfile

from subsets_utils import NodeSpec, SqlNodeSpec, save_raw_ndjson
from utils import get_bytes, latest_amce_url, read_zip_text


def fetch_amce_region(node_id: str) -> None:
    url = latest_amce_url()
    print(f"  AMCE region: downloading {url}")
    zf = zipfile.ZipFile(io.BytesIO(get_bytes(url)))
    region_files = sorted(
        n for n in zf.namelist() if re.fullmatch(r"region/[A-Za-z0-9]+\.csv", n)
    )
    if not region_files:
        raise AssertionError(f"no region/*.csv in AMCE zip {url}")
    rows: list[dict] = []
    for name in region_files:
        region = name[len("region/"):-len(".csv")]
        reader = csv.DictReader(read_zip_text(zf, name))
        for rec in reader:
            rec = {k: (v if v != "" else None) for k, v in rec.items()}
            rec["region"] = region
            rows.append(rec)
    save_raw_ndjson(rows, node_id)


DOWNLOAD_SPECS: list[NodeSpec] = [
    NodeSpec(id="wgms-amce-region", fn=fetch_amce_region, kind="download"),
]

TRANSFORM_SPECS: list[SqlNodeSpec] = [
    SqlNodeSpec(
        id="wgms-amce-region-transform",
        deps=["wgms-amce-region"],
        sql='''
            SELECT
                region,
                TRY_CAST(year AS INTEGER)      AS year,
                TRY_CAST(area_km2 AS DOUBLE)   AS area_km2,
                TRY_CAST(mwe AS DOUBLE)        AS mwe,
                TRY_CAST(mwe_sigma AS DOUBLE)  AS mwe_sigma,
                TRY_CAST(gt AS DOUBLE)         AS gt,
                TRY_CAST(gt_sigma AS DOUBLE)   AS gt_sigma
            FROM "wgms-amce-region"
            WHERE TRY_CAST(year AS INTEGER) IS NOT NULL
        ''',
    ),
]
