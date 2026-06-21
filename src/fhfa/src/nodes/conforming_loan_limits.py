"""Conforming loan limits — one county-level CSV per year (schema drifts:
underscore vs spaced/quoted headers, plain ints vs "$ ..." strings).

Discovered by probing a descending year window and keeping what returns 200.
"""

from __future__ import annotations

import io
import re

from subsets_utils import NodeSpec, SqlNodeSpec

from utils import (
    _clean_money,
    _current_year,
    _df_to_string_parquet,
    _get_optional,
)

CLL_URL = "https://www.fhfa.gov/document/d/cll/fullcountyloanlimitlist{year}_hera-based_final_flat.csv"
_CLL_RENAME = {
    "fips_state_code": "fips_state_code",
    "fips_county_code": "fips_county_code",
    "county_name": "county_name",
    "state": "state",
    "cbsa_number": "cbsa_number",
    "one_unit_limit": "one_unit_limit",
    "two_unit_limit": "two_unit_limit",
    "three_unit_limit": "three_unit_limit",
    "four_unit_limit": "four_unit_limit",
}


def _norm_cll_col(c: str) -> str:
    c = c.replace("﻿", "").strip().lower()
    c = re.sub(r"[\s\-]+", "_", c)  # collapse spaces / embedded newlines / hyphens
    return c


def fetch_conforming_loan_limits(node_id: str) -> None:
    import pandas as pd

    frames = []
    for year in range(_current_year() + 1, 2013, -1):
        resp = _get_optional(CLL_URL.format(year=year))
        if resp is None:
            continue
        df = pd.read_csv(
            io.BytesIO(resp.content),
            dtype=str,
            keep_default_na=False,
            na_values=[],
            encoding="utf-8-sig",
        )
        df.columns = [_norm_cll_col(c) for c in df.columns]
        df = df.rename(columns=_CLL_RENAME)
        for col in ("one_unit_limit", "two_unit_limit", "three_unit_limit", "four_unit_limit"):
            if col in df.columns:
                df[col] = df[col].map(_clean_money)
        df["year"] = str(year)
        keep = ["year"] + [c for c in _CLL_RENAME.values() if c in df.columns]
        frames.append(df[keep])
    if not frames:
        raise AssertionError("no conforming-loan-limit CSV files discovered")
    combined = pd.concat(frames, ignore_index=True)
    _df_to_string_parquet(combined, node_id)


DOWNLOAD_SPECS = [
    NodeSpec(id="fhfa-conforming-loan-limits", fn=fetch_conforming_loan_limits, kind="download"),
]

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="fhfa-conforming-loan-limits-transform",
        deps=["fhfa-conforming-loan-limits"],
        sql='''
            SELECT
                CAST(year AS INTEGER)                        AS year,
                fips_state_code,
                fips_county_code,
                county_name,
                state,
                cbsa_number,
                CAST(NULLIF(one_unit_limit, '') AS BIGINT)   AS one_unit_limit,
                CAST(NULLIF(two_unit_limit, '') AS BIGINT)   AS two_unit_limit,
                CAST(NULLIF(three_unit_limit, '') AS BIGINT) AS three_unit_limit,
                CAST(NULLIF(four_unit_limit, '') AS BIGINT)  AS four_unit_limit
            FROM "fhfa-conforming-loan-limits"
        ''',
    ),
]
