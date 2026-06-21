"""GDPplus — blended real output growth (real-time vintage matrix)."""

import re

import pyarrow as pa

from subsets_utils import NodeSpec, SqlNodeSpec

from utils import SND, _fetch_bytes, _read_xlsx, _write

_GDPPLUS_SCHEMA = pa.schema([
    ("period", pa.string()),
    ("vintage_date", pa.string()),
    ("gdpplus", pa.float64()),
])


def fetch_gdpplus(node_id: str) -> None:
    import pandas as pd
    url = f"{SND}/gdpplus/GDPplus_Vintages.xlsx"
    xl = _read_xlsx(_fetch_bytes(url))
    df = xl.parse(sheet_name=xl.sheet_names[0])
    date_col = df.columns[0]
    rows = []
    for _, r in df.iterrows():
        raw = r[date_col]
        if pd.isna(raw):
            continue
        # period 'YYYY:0Q' -> 'YYYY-QN'
        s = str(raw).strip()
        m = re.match(r"^(\d{4}):(\d{1,2})$", s)
        period = f"{m.group(1)}-Q{int(m.group(2))}" if m else s
        for c in df.columns[1:]:
            v = r[c]
            if pd.isna(v):
                continue
            vm = re.search(r"_(\d{6})$", str(c))  # GDPPLUS_MMDDYY
            if vm:
                mm, dd, yy = vm.group(1)[:2], vm.group(1)[2:4], vm.group(1)[4:6]
                year = 2000 + int(yy) if int(yy) < 70 else 1900 + int(yy)
                vintage = f"{year:04d}-{mm}-{dd}"
            else:
                vintage = str(c)
            rows.append({"period": period, "vintage_date": vintage, "gdpplus": float(v)})
    _write(rows, _GDPPLUS_SCHEMA, node_id)


DOWNLOAD_SPECS = [
    NodeSpec(id="philadelphia-fed-gdpplus", fn=fetch_gdpplus, kind="download"),
]

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="philadelphia-fed-gdpplus-transform",
        deps=["philadelphia-fed-gdpplus"],
        # Publish the most-recent-vintage growth series (one row per period). The
        # vintage_date is dropped: by construction the latest vintage is a single
        # release date covering all periods, so it would be a constant column.
        sql='''
            SELECT period, gdpplus AS gdpplus_growth
            FROM (
                SELECT period, gdpplus,
                       row_number() OVER (PARTITION BY period ORDER BY vintage_date DESC) AS rn
                FROM "philadelphia-fed-gdpplus"
                WHERE gdpplus IS NOT NULL
            )
            WHERE rn = 1
            ORDER BY period
        ''',
    ),
]
