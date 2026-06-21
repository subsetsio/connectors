"""Real-Time Data Set for Macroeconomists (RTDSM) — first/second/third releases."""

import re

import pyarrow as pa

from subsets_utils import NodeSpec, SqlNodeSpec

from utils import SND, _fetch_bytes, _fetch_html, _read_xlsx, _write

_RTDSM_INDEX = ("https://www.philadelphiafed.org/surveys-and-data/"
                "real-time-data-research/first-second-third")
_RTDSM_SCHEMA = pa.schema([
    ("variable", pa.string()),
    ("period", pa.string()),
    ("first_release", pa.float64()),
    ("second_release", pa.float64()),
    ("third_release", pa.float64()),
    ("most_recent", pa.float64()),
])


def _f(v):
    import pandas as pd
    return None if pd.isna(v) else float(v)


def fetch_real_time_data_set_macroeconomists(node_id: str) -> None:
    import pandas as pd
    # Discover the per-variable file set from the source page (auto-adapts to new vars).
    html = _fetch_html(_RTDSM_INDEX)
    files = sorted(set(re.findall(r"/-/media/[^\"'> ]*?/([a-z0-9_]+_first_second_third)\.xlsx", html, re.I)))
    if len(files) < 40:
        raise AssertionError(f"RTDSM: discovered only {len(files)} variable files (expected >=40)")
    base = f"{SND}/real-time-data/data-files/xlsx"
    rows = []
    for stem in files:
        variable = stem[:-len("_first_second_third")].upper()
        xl = _read_xlsx(_fetch_bytes(f"{base}/{stem}.xlsx"))
        raw = xl.parse(sheet_name="DATA", header=None)
        # find the header row whose first cell is 'Date'
        hdr = None
        for i in range(min(len(raw), 30)):
            if str(raw.iat[i, 0]).strip().lower() == "date":
                hdr = i
                break
        if hdr is None:
            raise AssertionError(f"RTDSM {stem}: no 'Date' header row found")
        for j in range(hdr + 1, len(raw)):
            period = raw.iat[j, 0]
            if pd.isna(period) or not str(period).strip():
                continue
            rows.append({
                "variable": variable,
                "period": str(period).strip().replace(":", "-"),
                "first_release": _f(raw.iat[j, 1]),
                "second_release": _f(raw.iat[j, 2]),
                "third_release": _f(raw.iat[j, 3]),
                "most_recent": _f(raw.iat[j, 4]),
            })
    _write(rows, _RTDSM_SCHEMA, node_id)


DOWNLOAD_SPECS = [
    NodeSpec(id="philadelphia-fed-real-time-data-set-macroeconomists", fn=fetch_real_time_data_set_macroeconomists, kind="download"),
]

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="philadelphia-fed-real-time-data-set-macroeconomists-transform",
        deps=["philadelphia-fed-real-time-data-set-macroeconomists"],
        sql='''
            SELECT variable, period,
                   first_release, second_release, third_release, most_recent
            FROM "philadelphia-fed-real-time-data-set-macroeconomists"
            WHERE coalesce(first_release, second_release, third_release, most_recent) IS NOT NULL
            ORDER BY variable, period
        ''',
    ),
]
