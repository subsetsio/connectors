"""Annual Mass-Change Estimates (AMCE) — global aggregate.

A derived product (Dussaillant et al. 2025, ESSD) downscaling FoG observations
to an annual mass-change series. The globally-aggregated `global.csv` is small
and clean, so it is saved as raw CSV directly.
"""

from __future__ import annotations

import io
import zipfile

from subsets_utils import NodeSpec, SqlNodeSpec, save_raw_file
from utils import get_bytes, latest_amce_url


def fetch_amce_global(node_id: str) -> None:
    url = latest_amce_url()
    print(f"  AMCE global: downloading {url}")
    zf = zipfile.ZipFile(io.BytesIO(get_bytes(url)))
    with zf.open("global.csv") as fh:
        save_raw_file(fh.read().decode("utf-8"), node_id, extension="csv")


_DOWNLOAD_SPECS: list[NodeSpec] = [
    NodeSpec(id="wgms-amce-global", fn=fetch_amce_global, kind="download"),
]

TRANSFORM_SPECS: list[SqlNodeSpec] = [
    SqlNodeSpec(
        id="wgms-amce-global-transform",
        deps=["wgms-amce-global"],
        sql='''
            SELECT
                TRY_CAST(year AS INTEGER)               AS year,
                TRY_CAST(area_km2 AS DOUBLE)            AS area_km2,
                TRY_CAST(mwe AS DOUBLE)                 AS mwe,
                TRY_CAST(mwe_sigma AS DOUBLE)           AS mwe_sigma,
                TRY_CAST(mwe_cumsum AS DOUBLE)          AS mwe_cumsum,
                TRY_CAST(gt AS DOUBLE)                  AS gt,
                TRY_CAST(gt_sigma AS DOUBLE)            AS gt_sigma,
                TRY_CAST(gt_cumsum AS DOUBLE)           AS gt_cumsum,
                TRY_CAST(gt_cumsum_sigma AS DOUBLE)     AS gt_cumsum_sigma,
                TRY_CAST(mmsle AS DOUBLE)               AS mmsle,
                TRY_CAST(mmsle_sigma AS DOUBLE)         AS mmsle_sigma,
                TRY_CAST(mmsle_cumsum AS DOUBLE)        AS mmsle_cumsum,
                TRY_CAST(mmsle_cumsum_sigma AS DOUBLE)  AS mmsle_cumsum_sigma
            FROM "wgms-amce-global"
            WHERE TRY_CAST(year AS INTEGER) IS NOT NULL
        ''',
    ),
]
