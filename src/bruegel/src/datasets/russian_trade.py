"""Russian Foreign Trade Tracker — multi-figure Excel workbook with a
"direction of trade" header row per figure sheet, flattened to long."""
import datetime
import io
import re

import pandas as pd

from subsets_utils import NodeSpec, SqlNodeSpec
from utils import clean, get_bytes, run_download, xlsx_link

EID = "russian-foreign-trade-tracker"
DEP = f"bruegel-{EID}"
PAGE_PATH = "/dataset/russian-foreign-trade-tracker"

_RU_STD_SHEETS = ["Figure 1", "Figure 2", "Figure 3", "Figure 4",
                  "Figure 5", "Figure 8&9", "Figure 10"]

# Sheet "Figure 8&9" stacks two figures under one header ("Figure 8: ... mineral
# fuels", then "Figure 9: ... goods other than mineral fuels"). Each block is
# introduced by its own title row, so track the marker and label rows with the
# figure they actually came from rather than the sheet name.
_FIG_RE = re.compile(r"^\s*(Figure\s+\d+)\s*:", re.I)


def _figure_marker(cell) -> str | None:
    m = _FIG_RE.match(str(cell))
    return m.group(1).title() if m else None


def parse(links):
    xl = pd.ExcelFile(io.BytesIO(get_bytes(xlsx_link(links))))
    out = []
    for sheet in _RU_STD_SHEETS:
        if sheet not in xl.sheet_names:
            continue
        raw = xl.parse(sheet, header=None)
        hdr = None
        for i in range(min(10, len(raw))):
            if str(raw.iloc[i, 0]).strip().lower() == "direction of trade":
                hdr = i
                break
        if hdr is None:
            continue
        header = raw.iloc[hdr].tolist()
        date_cols, dim_cols = [], []
        for ci, h in enumerate(header):
            if isinstance(h, (datetime.datetime, pd.Timestamp)):
                date_cols.append(ci)
            elif pd.notna(h) and not date_cols:
                dim_cols.append(ci)
        dim_names = [str(header[ci]).strip() for ci in dim_cols]
        # the block the header belongs to is titled above it; later blocks retitle
        # themselves inside the body
        figure = next((f for f in (_figure_marker(c) for c in raw.iloc[:hdr, 0]) if f), sheet)
        body = raw.iloc[hdr + 1:]
        for _, row in body.iterrows():
            c0 = row.iloc[0]
            if pd.isna(c0) or str(c0).strip() == "":
                continue
            if str(c0).strip().lower().startswith(("source:", "figure")):
                figure = _figure_marker(c0) or figure
                continue
            dims = {dim_names[k]: row.iloc[dim_cols[k]] for k in range(len(dim_cols))}
            for dc in date_cols:
                val = row.iloc[dc]
                if pd.isna(val):
                    continue
                try:
                    v = float(val)
                except (ValueError, TypeError):
                    continue
                out.append({
                    "figure": figure,
                    "date": pd.Timestamp(header[dc]).date().isoformat(),
                    "direction_of_trade": clean(dims.get("direction of trade")),
                    "country": clean(dims.get("country")),
                    "unit": clean(dims.get("unit")),
                    "sitc_code": clean(dims.get("SITC 1-digit code")
                                       or dims.get("SITC 2-digit code")),
                    "sitc_category": clean(dims.get("SITC category description")),
                    "value": v,
                })
    return out


def fetch(node_id: str) -> None:
    run_download(node_id, PAGE_PATH, parse)


DOWNLOAD_SPECS = [NodeSpec(id=DEP, fn=fetch, kind="download")]

_SQL = '''
        SELECT figure, CAST(date AS DATE) AS date, direction_of_trade,
               country, unit, sitc_code, sitc_category,
               CAST(value AS DOUBLE) AS value
        FROM "{dep}" WHERE value IS NOT NULL
    '''

TRANSFORM_SPECS = [SqlNodeSpec(id=f"{DEP}-transform", deps=[DEP],
                               sql=_SQL.replace("{dep}", DEP))]
