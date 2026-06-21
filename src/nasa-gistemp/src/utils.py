"""Shared transport + parsing for NASA GISTEMP v4 table downloads.

Source: https://data.giss.nasa.gov/gistemp/tabledata_v4/ (NASA GISS Surface
Temperature Analysis, v4). Combined land-surface-air + sea-surface-water
temperature anomalies, in degrees Celsius vs the 1951-1980 base period.

Parsing notes (verified against the live API 2026-06):
  - Values are ALREADY decimal degrees Celsius (e.g. '-.19', '1.25'). Do NOT
    divide by 100 — the legacy climate-indicators connector did, which is wrong
    for these .csv files.
  - Missing/not-yet-available cells are '***' (occasionally '****'); -> null.
"""

import csv
import io

from subsets_utils import get, transient_retry

BASE_URL = "https://data.giss.nasa.gov/gistemp/tabledata_v4"

# Combined land-ocean (.Ts+dSST) tables, one per region. region is a column value.
REGION_FILES = [
    ("GLB.Ts+dSST.csv", "Global"),
    ("NH.Ts+dSST.csv", "Northern Hemisphere"),
    ("SH.Ts+dSST.csv", "Southern Hemisphere"),
]


# --- transport -------------------------------------------------------------


@transient_retry()
def _fetch_csv(filename: str) -> str:
    resp = get(f"{BASE_URL}/{filename}", timeout=(10.0, 120.0))
    resp.raise_for_status()
    return resp.text


# --- parsing ---------------------------------------------------------------

def _parse_anomaly(s: str):
    """GISTEMP anomaly cell -> float degrees C, or None for missing markers."""
    s = (s or "").strip()
    if not s or s == "-" or set(s) <= {"*"}:
        return None
    return float(s)


def _read_table(content: str):
    """Return (header, data_rows). GISS files carry a one-line descriptive
    header before the real 'Year,...' header row; skip until that row."""
    rows = list(csv.reader(io.StringIO(content)))
    header_idx = next(i for i, r in enumerate(rows) if r and r[0].strip() == "Year")
    header = [h.strip() for h in rows[header_idx]]
    data = [r for r in rows[header_idx + 1:] if r and r[0].strip().isdigit()]
    return header, data
