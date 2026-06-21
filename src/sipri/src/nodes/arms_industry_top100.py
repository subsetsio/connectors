"""SIPRI arms industry Top 100 — per-company-year panel of the SIPRI Top 100,
parsed from the Top-100 .xlsx (one sheet per year). Stateless full re-pull
(SIPRI revises prior years on every annual release).
"""

import re

import pyarrow as pa

from subsets_utils import NodeSpec, SqlNodeSpec, save_raw_parquet
from utils import find_xlsx, isnum, load_wb

_TOP100_SCHEMA = pa.schema([
    ("year", pa.int32()),
    ("rank", pa.int32()),
    ("company", pa.string()),
    ("country", pa.string()),
    ("arms_revenue_musd", pa.float64()),
    ("total_revenue_musd", pa.float64()),
    ("arms_share_of_total", pa.float64()),
])


def fetch_arms_industry_top100(node_id: str) -> None:
    asset = node_id
    url = find_xlsx("/databases/armsindustry", "Top-100")
    wb = load_wb(url)
    out = []
    year_sheets = [sn for sn in wb.sheetnames if re.fullmatch(r"\d{4}", sn.strip())]
    if not year_sheets:
        raise RuntimeError("Top-100 workbook has no year-named sheets")
    for sn in year_sheets:
        yr = int(sn.strip())
        rows = list(wb[sn].iter_rows(values_only=True))
        hdr = next(
            (i for i, r in enumerate(rows)
             if r and isinstance(r[0], str) and r[0].strip().startswith("Rank")),
            None,
        )
        if hdr is None:
            raise RuntimeError(f"Top-100 sheet '{sn}': no 'Rank' header row found")
        h = [(str(c).strip() if c is not None else "") for c in rows[hdr]]

        def find(pred):
            return next((j for j, t in enumerate(h) if pred(t)), None)

        c_rank = find(lambda t: t.startswith("Rank") and str(yr) in t)
        c_co = find(lambda t: t.startswith("Company"))
        c_country = find(lambda t: t.strip().startswith("Country"))
        c_arms = find(lambda t: t.startswith("Arms revenues") and str(yr) in t
                      and "constant" not in t.lower() and "%" not in t)
        c_total = find(lambda t: t.startswith("Total revenues"))
        c_share = find(lambda t: "as a %" in t)
        if c_co is None or c_arms is None:
            raise RuntimeError(f"Top-100 sheet '{sn}': could not locate company/arms-revenue columns; header={h}")

        def cell(r, c):
            return r[c] if c is not None and c < len(r) else None

        for r in rows[hdr + 1:]:
            co = cell(r, c_co)
            rk = cell(r, c_rank)
            if not (isinstance(co, str) and co.strip()) or not isnum(rk):
                continue  # footnote / blank rows have no numeric rank
            country = cell(r, c_country)
            out.append({
                "year": yr,
                "rank": int(rk),
                "company": co.strip(),
                "country": country.strip() if isinstance(country, str) and country.strip() else None,
                "arms_revenue_musd": float(cell(r, c_arms)) if isnum(cell(r, c_arms)) else None,
                "total_revenue_musd": float(cell(r, c_total)) if isnum(cell(r, c_total)) else None,
                "arms_share_of_total": float(cell(r, c_share)) if isnum(cell(r, c_share)) else None,
            })
    if not out:
        raise RuntimeError("arms-industry-top100 parse produced 0 rows")
    save_raw_parquet(pa.Table.from_pylist(out, schema=_TOP100_SCHEMA), asset)


DOWNLOAD_SPECS = [
    NodeSpec(id="sipri-arms-industry-top100", fn=fetch_arms_industry_top100, kind="download"),
]

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="sipri-arms-industry-top100-transform",
        deps=["sipri-arms-industry-top100"],
        sql='''
            SELECT
                CAST(year AS INTEGER) AS year,
                CAST(rank AS INTEGER) AS rank,
                company,
                country,
                CAST(arms_revenue_musd AS DOUBLE)    AS arms_revenue_musd,
                CAST(total_revenue_musd AS DOUBLE)   AS total_revenue_musd,
                CAST(arms_share_of_total AS DOUBLE)  AS arms_share_of_total
            FROM "sipri-arms-industry-top100"
            WHERE company IS NOT NULL
        ''',
    ),
]
