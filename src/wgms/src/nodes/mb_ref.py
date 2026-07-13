"""mb_ref.csv — a small pre-aggregated reference-glacier summary.

A standalone CSV served directly from a stable URL (no zip, no listing page).
"""

from __future__ import annotations

from subsets_utils import NodeSpec, SqlNodeSpec, save_raw_file
from utils import get_text

MB_REF_URL = "https://wgms.ch/data/faq/mb_ref.csv"


def fetch_mb_ref(node_id: str) -> None:
    print(f"  mb_ref: downloading {MB_REF_URL}")
    save_raw_file(get_text(MB_REF_URL), node_id, extension="csv")


_DOWNLOAD_SPECS: list[NodeSpec] = [
    NodeSpec(id="wgms-mb-ref", fn=fetch_mb_ref, kind="download"),
]

TRANSFORM_SPECS: list[SqlNodeSpec] = [
    SqlNodeSpec(
        id="wgms-mb-ref-transform",
        deps=["wgms-mb-ref"],
        sql='''
            SELECT
                TRY_CAST("Year" AS INTEGER)         AS year,
                TRY_CAST(MB_REF_count AS INTEGER)   AS reference_glacier_count,
                TRY_CAST(REF_regionAVG AS DOUBLE)   AS annual_mass_balance_mm_we,
                TRY_CAST("REF_regionAVG_cum-rel-1970" AS DOUBLE)
                                                    AS cumulative_mass_balance_mm_we_rel_1970
            FROM "wgms-mb-ref"
            WHERE TRY_CAST("Year" AS INTEGER) IS NOT NULL
        ''',
    ),
]
