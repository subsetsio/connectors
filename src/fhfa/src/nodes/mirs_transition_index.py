"""MIRS Transition Index — tiny stable monthly CSV (date, value)."""

from __future__ import annotations

import io

from subsets_utils import NodeSpec, SqlNodeSpec

from utils import _df_to_string_parquet, _get

MIRS_URL = "https://www.fhfa.gov/document/d/mirs/mirs-historical-data-file"


def fetch_mirs_transition_index(node_id: str) -> None:
    import pandas as pd

    resp = _get(MIRS_URL)
    df = pd.read_csv(
        io.BytesIO(resp.content),
        dtype=str,
        keep_default_na=False,
        na_values=[],
        encoding="utf-8-sig",
    )
    if df.shape[1] < 2:
        raise AssertionError(f"MIRS file has {df.shape[1]} columns, expected >=2")
    df = df.iloc[:, :2]
    df.columns = ["release_date", "index_value"]
    df["release_date"] = df["release_date"].str.strip()
    df["index_value"] = df["index_value"].str.strip()
    _df_to_string_parquet(df, node_id)


DOWNLOAD_SPECS = []

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="fhfa-mirs-transition-index-transform",
        deps=["fhfa-mirs-transition-index"],
        sql='''
            SELECT
                CAST(strptime(trim(release_date), '%m/%d/%Y') AS DATE) AS date,
                CAST(NULLIF(index_value, '') AS DOUBLE)                AS index_value
            FROM "fhfa-mirs-transition-index"
            WHERE NULLIF(release_date, '') IS NOT NULL
        ''',
    ),
]
