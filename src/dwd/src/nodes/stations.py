"""DWD stations metadata — joinable reference (from the daily/kl master list).

A single joinable station-metadata reference parsed from the fixed-layout
KL_Tageswerte_Beschreibung_Stationen.txt description file.

Stateless full re-pull every refresh: the server overwrites the file in place and
exposes no since/cursor delta.
"""

import pyarrow as pa

from subsets_utils import NodeSpec, SqlNodeSpec, save_raw_parquet
from utils import OBS, _get_text

_STATIONS_URL = f"{OBS}/daily/kl/historical/KL_Tageswerte_Beschreibung_Stationen.txt"
_STATIONS_SCHEMA = pa.schema([
    ("station_id", pa.int32()),
    ("from_date", pa.string()),
    ("to_date", pa.string()),
    ("height_m", pa.float64()),
    ("latitude", pa.float64()),
    ("longitude", pa.float64()),
    ("name", pa.string()),
    ("bundesland", pa.string()),
])


def fetch_stations(node_id: str) -> None:
    text = _get_text(_STATIONS_URL, encoding="latin-1")
    lines = text.splitlines()
    # line 0 = header, line 1 = dashes separator, rest = fixed-layout rows.
    out = {c: [] for c in _STATIONS_SCHEMA.names}
    for ln in lines[2:]:
        if not ln.strip():
            continue
        tok = ln.split()
        # leading 6 numeric tokens; trailing 2 = Bundesland, Abgabe; middle = name
        if len(tok) < 8:
            continue
        try:
            sid = int(tok[0])
        except ValueError:
            continue
        name = " ".join(tok[6:-2]) if len(tok) > 8 else tok[6]
        out["station_id"].append(sid)
        out["from_date"].append(tok[1])
        out["to_date"].append(tok[2])
        out["height_m"].append(_f(tok[3]))
        out["latitude"].append(_f(tok[4]))
        out["longitude"].append(_f(tok[5]))
        out["name"].append(name)
        out["bundesland"].append(tok[-2])
    if len(out["station_id"]) < 100:
        raise RuntimeError(f"stations: only {len(out['station_id'])} parsed; layout likely changed")
    save_raw_parquet(pa.table(out, schema=_STATIONS_SCHEMA), node_id)


def _f(s: str):
    try:
        return float(s)
    except ValueError:
        return None


_STATIONS_SQL = '''
    SELECT station_id, from_date, to_date, height_m, latitude, longitude, name, bundesland
    FROM "{dep}"
    WHERE station_id IS NOT NULL
'''

DOWNLOAD_SPECS = []

TRANSFORM_SPECS = []
