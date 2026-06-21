"""Shared transport, parsing, and schema helpers for the PSMSL connector.

Access is three persistent bulk ZIPs; each unpacks to one ';'-delimited file per
station under <product>/data/<id>.<ext> plus a single <product>/filelist.txt of
station metadata. Data-file rows are 4 ';'-separated columns:
time; msl_mm; flag3; flag4. MSL is in millimetres relative to the station datum;
-99999 means missing.
"""

import io
import zipfile

import pyarrow as pa

from subsets_utils import get, transient_retry

# --- ZIP URLs per product -------------------------------------------------
RLR_MONTHLY_ZIP = "https://psmsl.org/data/obtaining/rlr.monthly.data/rlr_monthly.zip"
RLR_ANNUAL_ZIP = "https://psmsl.org/data/obtaining/rlr.annual.data/rlr_annual.zip"
MET_MONTHLY_ZIP = "https://psmsl.org/data/obtaining/met.monthly.data/met_monthly.zip"

MISSING = -99999


# --- transport ------------------------------------------------------------
@transient_retry()
def download_zip(url: str) -> zipfile.ZipFile:
    resp = get(url, timeout=(10.0, 300.0))
    resp.raise_for_status()
    return zipfile.ZipFile(io.BytesIO(resp.content))


# --- parsing helpers ------------------------------------------------------
def station_id_from_path(path: str) -> int:
    stem = path.rsplit("/", 1)[-1].rsplit(".", 1)[0]
    return int(stem)


def parse_value(token: str):
    v = int(token)
    return None if v == MISSING else float(v)


def data_members(zf: zipfile.ZipFile, ext: str):
    """Yield (station_id, lines) for every per-station data file in the ZIP."""
    for name in zf.namelist():
        if name.endswith(ext) and "/data/" in name:
            text = zf.read(name).decode("latin-1")
            yield station_id_from_path(name), text.splitlines()


def month_from_decimal(decimal_year: float, year: int) -> int:
    # PSMSL monthly midpoints: decimal_year = year + (month - 0.5) / 12
    return int(round((decimal_year - year) * 12 + 0.5))


# --- monthly schema + parser (shared by rlr-monthly and met-monthly) ------
MONTHLY_SCHEMA = pa.schema(
    [
        ("station_id", pa.int32()),
        ("decimal_year", pa.float64()),
        ("year", pa.int32()),
        ("month", pa.int32()),
        ("msl_mm", pa.float64()),
        ("missing_flag", pa.string()),
        ("data_flag", pa.string()),
    ]
)


def parse_monthly(zf: zipfile.ZipFile, ext: str) -> list[dict]:
    rows = []
    for sid, lines in data_members(zf, ext):
        for line in lines:
            line = line.strip()
            if not line:
                continue
            parts = [p.strip() for p in line.split(";")]
            decimal_year = float(parts[0])
            year = int(decimal_year)
            rows.append(
                {
                    "station_id": sid,
                    "decimal_year": decimal_year,
                    "year": year,
                    "month": month_from_decimal(decimal_year, year),
                    "msl_mm": parse_value(parts[1]),
                    "missing_flag": parts[2] if len(parts) > 2 else None,
                    "data_flag": parts[3] if len(parts) > 3 else None,
                }
            )
    return rows


# --- monthly transform SQL (shared by rlr-monthly and met-monthly) --------
MONTHLY_SQL = """
    SELECT
        station_id,
        make_date(year, month, 1) AS date,
        year,
        month,
        decimal_year,
        msl_mm,
        missing_flag,
        data_flag
    FROM "{dep}"
    WHERE msl_mm IS NOT NULL
"""
