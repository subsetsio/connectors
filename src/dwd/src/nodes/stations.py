"""DWD stations metadata — joinable reference (from the daily/kl master list).

A single joinable station-metadata reference parsed from the fixed-layout
KL_Tageswerte_Beschreibung_Stationen.txt description file.

Stateless full re-pull every refresh: the server overwrites the file in place and
exposes no since/cursor delta.
"""

import re
from datetime import datetime

import pyarrow as pa

from subsets_utils import NodeSpec, SqlNodeSpec, save_raw_parquet
from utils import OBS, _get_text

_STATIONS_URL = f"{OBS}/daily/kl/historical/KL_Tageswerte_Beschreibung_Stationen.txt"
_STATIONS_SCHEMA = pa.schema([
    ("station_id", pa.int32()),
    ("from_date", pa.date32()),
    ("to_date", pa.date32()),
    ("height_m", pa.float64()),
    ("latitude", pa.float64()),
    ("longitude", pa.float64()),
    ("name", pa.string()),
    ("bundesland", pa.string()),
])


# The six leading numeric fields, whitespace-separated and never empty.
_PREFIX = re.compile(
    r"^\s*(\d+)\s+(\d{8})\s+(\d{8})\s+(-?\d+(?:\.\d+)?)\s+(-?\d+\.\d+)\s+(-?\d+\.\d+)\s"
)


def fetch_stations(node_id: str) -> None:
    text = _get_text(_STATIONS_URL, encoding="latin-1")
    lines = text.splitlines()
    # line 0 = header, line 1 = dashes separator, rest = fixed-layout rows.
    out = {c: [] for c in _STATIONS_SCHEMA.names}
    for ln in lines[2:]:
        if not ln.strip():
            continue
        m = _PREFIX.match(ln)
        if not m:
            continue
        # The dashes separator understates the real column widths, and the
        # trailing Abgabe field is empty on ~5% of rows, so neither fixed
        # offsets nor token counting from the right survive. The name/
        # Bundesland/Abgabe fields are space-padded, and no station name
        # contains a run of two spaces, so 2+ spaces is the field separator.
        tail = [p for p in re.split(r"\s{2,}", ln[m.end():].strip()) if p]
        if len(tail) < 2:
            continue
        out["station_id"].append(int(m.group(1)))
        out["from_date"].append(_d(m.group(2)))
        out["to_date"].append(_d(m.group(3)))
        out["height_m"].append(_f(m.group(4)))
        out["latitude"].append(_f(m.group(5)))
        out["longitude"].append(_f(m.group(6)))
        out["name"].append(tail[0])
        out["bundesland"].append(tail[1])
    if len(out["station_id"]) < 100:
        raise RuntimeError(f"stations: only {len(out['station_id'])} parsed; layout likely changed")
    n_bl = len(set(out["bundesland"]))
    if n_bl != 16:
        raise RuntimeError(f"stations: {n_bl} distinct Bundesland values, expected Germany's 16; layout likely changed")
    save_raw_parquet(pa.table(out, schema=_STATIONS_SCHEMA), node_id)


def _f(s: str):
    try:
        return float(s)
    except ValueError:
        return None


def _d(s: str):
    try:
        return datetime.strptime(s, "%Y%m%d").date()
    except ValueError:
        return None

DOWNLOAD_SPECS = []

TRANSFORM_SPECS = []
