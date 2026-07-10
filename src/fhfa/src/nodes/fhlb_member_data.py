"""Federal Home Loan Bank membership data."""

from __future__ import annotations

import io
import re

from subsets_utils import NodeSpec

from utils import _df_to_string_parquet, _get

FHLB_MEMBERS_PAGE = "https://www.fhfa.gov/data/fhlb-membership"


def _latest_workbook_url() -> str:
    page = _get(FHLB_MEMBERS_PAGE).text
    match = re.search(r'href="([^"]+fhlb[_-]members[^"]+\.xlsx)"', page, flags=re.I)
    if not match:
        raise AssertionError("no FHLB members XLSX link found")
    href = match.group(1)
    return href if href.startswith("http") else f"https://www.fhfa.gov{href}"


def _norm_col(col: object) -> str:
    s = str(col).replace("\ufeff", "").strip().lower()
    s = re.sub(r"[^a-z0-9]+", "_", s).strip("_")
    return s or "unnamed"


def _period_from_url(url: str) -> str | None:
    match = re.search(r"q([1-4])[\-_]?(20\d{2})", url, flags=re.I)
    return f"{match.group(2)}Q{match.group(1)}" if match else None


def fetch_fhlb_member_data(node_id: str) -> None:
    import pandas as pd

    url = _latest_workbook_url()
    resp = _get(url)
    df = pd.read_excel(
        io.BytesIO(resp.content),
        sheet_name="MembershipOpenGovt",
        dtype=str,
        keep_default_na=False,
        na_values=[],
    )
    df = df.rename(columns={c: _norm_col(c) for c in df.columns})
    df["release_period"] = _period_from_url(url)
    df["source_url"] = url
    _df_to_string_parquet(df, node_id)


DOWNLOAD_SPECS = []
