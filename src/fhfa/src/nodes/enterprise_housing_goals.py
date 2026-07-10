"""Enterprise Housing Goals — wide per-year state table (metric_<year>
columns, %/$ strings). Melt to a tidy long (state, year, metric, value)."""

from __future__ import annotations

import io
import re

from subsets_utils import NodeSpec, SqlNodeSpec

from utils import (
    _clean_money,
    _current_year,
    _df_to_string_parquet,
    _get_optional,
    _unzip_single_csv,
)

EHG_URL = "https://www.fhfa.gov/document/d/ehg/enterprise_housing_goals_state_data_{year}.zip"


def _norm_metric(c: str, year: int) -> str:
    c = c.replace("﻿", "").strip()
    c = re.sub(rf"_{year}$", "", c)  # drop the trailing _<year>
    c = re.sub(r"[\s]+", "_", c).lower()
    return c


def fetch_enterprise_housing_goals(node_id: str) -> None:
    import pandas as pd

    frames = []
    for year in range(_current_year() + 1, 2008, -1):
        resp = _get_optional(EHG_URL.format(year=year))
        if resp is None:
            continue
        csv_bytes = _unzip_single_csv(resp.content)
        df = pd.read_csv(
            io.BytesIO(csv_bytes),
            dtype=str,
            keep_default_na=False,
            na_values=[],
            encoding="utf-8-sig",
        )
        df.columns = [_norm_metric(c, year) for c in df.columns]
        if "state" not in df.columns:
            raise AssertionError(f"EHG {year}: no STATE column after normalize ({list(df.columns)[:3]})")
        long = df.melt(id_vars=["state"], var_name="metric", value_name="value")
        long["value"] = long["value"].map(_clean_money)  # strip %, $, commas
        long["year"] = str(year)
        frames.append(long[["state", "year", "metric", "value"]])
    if not frames:
        raise AssertionError("no enterprise-housing-goals files discovered")
    combined = pd.concat(frames, ignore_index=True)
    _df_to_string_parquet(combined, node_id)


DOWNLOAD_SPECS = []

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="fhfa-enterprise-housing-goals-transform",
        deps=["fhfa-enterprise-housing-goals"],
        sql='''
            SELECT
                state,
                CAST(year AS INTEGER)               AS year,
                metric,
                CAST(NULLIF(value, '') AS DOUBLE)   AS value
            FROM "fhfa-enterprise-housing-goals"
        ''',
    ),
]
