"""Annual Mass-Change Estimates (AMCE) — per glacier.

Per-glacier annual mass change covering ~216k glaciers. The `_mwe.csv` files are
WIDE (one column per year); unpivot to long and join each region's metadata,
writing one streamed ndjson batch per region (region becomes a column). Memory
stays bounded by the per-region metadata dict — the wide mwe file is streamed.
"""

from __future__ import annotations

import io
import json
import re
import zipfile
import csv

from subsets_utils import NodeSpec, SqlNodeSpec, raw_writer
from utils import get_bytes, latest_amce_url, read_zip_text


def fetch_amce_glacier(node_id: str) -> None:
    url = latest_amce_url()
    print(f"  AMCE glacier: downloading {url}")
    zf = zipfile.ZipFile(io.BytesIO(get_bytes(url)))
    names = set(zf.namelist())
    regions = sorted(
        m.group(1)
        for n in names
        if (m := re.fullmatch(r"glacier/([A-Za-z0-9]+)_mwe\.csv", n))
    )
    if not regions:
        raise AssertionError(f"no glacier/*_mwe.csv in AMCE zip {url}")

    for region in regions:
        meta_name = f"glacier/{region}_metadata.csv"
        mwe_name = f"glacier/{region}_mwe.csv"
        meta: dict[str, dict] = {}
        if meta_name in names:
            for rec in csv.DictReader(read_zip_text(zf, meta_name)):
                meta[rec["outline_id"]] = rec

        # batch_key is pure batch info (the region code); transform globs
        # 'wgms-amce-glacier-*' to union every region batch.
        batch_asset = f"{node_id}-{region}"
        with raw_writer(batch_asset, "ndjson.gz", mode="wt", compression="gzip") as out:
            reader = csv.reader(read_zip_text(zf, mwe_name))
            header = next(reader)  # outline_id, <year>, <year>, ...
            years = header[1:]
            for row in reader:
                outline_id = row[0]
                m = meta.get(outline_id, {})
                for yi, year in enumerate(years, start=1):
                    if yi >= len(row):
                        break
                    val = row[yi]
                    if val == "":
                        continue
                    out.write(json.dumps({
                        "region": region,
                        "outline_id": outline_id,
                        "glacier_id": m.get("glacier_id"),
                        "latitude": m.get("latitude"),
                        "longitude": m.get("longitude"),
                        "area_km2": m.get("area_km2"),
                        "year": year,
                        "mwe": val,
                    }) + "\n")


_DOWNLOAD_SPECS: list[NodeSpec] = [
    NodeSpec(id="wgms-amce-glacier", fn=fetch_amce_glacier, kind="download"),
]

TRANSFORM_SPECS: list[SqlNodeSpec] = [
    SqlNodeSpec(
        id="wgms-amce-glacier-transform",
        deps=["wgms-amce-glacier"],
        sql='''
            SELECT
                region,
                outline_id,
                TRY_CAST(glacier_id AS BIGINT) AS glacier_id,
                TRY_CAST(latitude AS DOUBLE)   AS latitude,
                TRY_CAST(longitude AS DOUBLE)  AS longitude,
                TRY_CAST(area_km2 AS DOUBLE)   AS area_km2,
                TRY_CAST(year AS INTEGER)      AS year,
                TRY_CAST(mwe AS DOUBLE)        AS mwe
            FROM "wgms-amce-glacier"
            WHERE TRY_CAST(year AS INTEGER) IS NOT NULL
              AND mwe IS NOT NULL
        ''',
    ),
]
