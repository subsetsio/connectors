"""DWD regional (Bundesland) averages — long-format, one table per resolution.

Area-mean (Bundesland) climate series — the cleanest national statistics — melted
to long (variable, region, year, period). One parametric fetcher
(`fetch_regional`) drives each resolution (annual/monthly/seasonal) from the
`_REGIONAL` table.

Stateless full re-pull every refresh: the server overwrites files in place and
exposes no since/cursor delta.
"""

import pyarrow as pa

from subsets_utils import NodeSpec, SqlNodeSpec, save_raw_parquet
from utils import REG, _get_text, _list_hrefs

# DWD missing-value sentinels appear as -999 in the regional-average CSVs;
# treated as NULL (skipped).
_MISSING = {"", "-999", "-999.0"}

_REGIONAL = {
    "dwd-regional-annual": "annual",
    "dwd-regional-monthly": "monthly",
    "dwd-regional-seasonal": "seasonal",
}

_REG_SCHEMA = pa.schema([
    ("variable", pa.string()),  # e.g. air_temperature_mean, precipitation, frost_days
    ("region", pa.string()),    # Bundesland or combination, incl. "Deutschland"
    ("year", pa.int32()),
    ("period", pa.string()),    # "year" | month number | season name
    ("value", pa.float64()),
])


def fetch_regional(node_id: str) -> None:
    resolution = _REGIONAL[node_id]
    variables = [h.rstrip("/") for h in _list_hrefs(f"{REG}/{resolution}/") if h.endswith("/")]
    if not variables:
        raise RuntimeError(f"{node_id}: no variable dirs under {REG}/{resolution}/")

    out = {c: [] for c in _REG_SCHEMA.names}
    n_files = 0
    for var in variables:
        vdir = f"{REG}/{resolution}/{var}/"
        txts = [h for h in _list_hrefs(vdir) if h.endswith(".txt")]
        for txt in txts:
            text = _get_text(vdir + txt, encoding="latin-1")
            lines = [ln for ln in text.splitlines() if ln.strip()]
            if len(lines) < 3:
                continue
            # line 0 = free-text title; line 1 = header (Jahr;<period>;<regions...>)
            head = [c.strip() for c in lines[1].split(";")]
            regions = [r for r in head[2:] if r]  # drop trailing empty from final ';'
            for ln in lines[2:]:
                cells = [c.strip() for c in ln.split(";")]
                if len(cells) < 2 + len(regions):
                    continue
                try:
                    year = int(cells[0])
                except ValueError:
                    continue
                period = cells[1]
                for k, region in enumerate(regions):
                    raw = cells[2 + k]
                    if raw in _MISSING:
                        continue
                    try:
                        val = float(raw)
                    except ValueError:
                        continue
                    if val == -999:
                        continue
                    out["variable"].append(var)
                    out["region"].append(region)
                    out["year"].append(year)
                    out["period"].append(period)
                    out["value"].append(val)
            n_files += 1
    if not out["value"]:
        raise RuntimeError(f"{node_id}: parsed 0 values across {n_files} files")
    save_raw_parquet(pa.table(out, schema=_REG_SCHEMA), node_id)


_REG_SQL = '''
    SELECT variable, region, CAST(year AS INTEGER) AS year, period, CAST(value AS DOUBLE) AS value
    FROM "{dep}"
    WHERE value IS NOT NULL
'''

DOWNLOAD_SPECS = [NodeSpec(id=sid, fn=fetch_regional, kind="download") for sid in _REGIONAL]

TRANSFORM_SPECS = [
    SqlNodeSpec(id=f"{sid}-transform", deps=[sid], sql=_REG_SQL.format(dep=sid)) for sid in _REGIONAL
]
