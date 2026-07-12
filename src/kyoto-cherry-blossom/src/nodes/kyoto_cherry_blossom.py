"""Kyoto cherry-blossom bloom series — Aono & Kazui / Aono & Saito record.

Two small, fully-snapshotable subsets, so both fetch fns are stateless full
re-pulls (shape 1): the whole file is fetched and overwritten every run. Each
file is a few tens of KB, so there is no need for watermarks or incrementality.

- bloom-dates: the peak full-flowering day-of-year series, from Our World in
  Data's CC-BY republication (the maintained version, current through 2026).
- temperature-reconstruction: the reconstructed + observed March mean
  temperature series, from the NOAA NCEI paleoclimatology archive (study 26430,
  a frozen snapshot ending 2005). Distinct schema from the bloom series.
"""

import csv
import io

import pyarrow as pa
from subsets_utils import NodeSpec, get, save_raw_parquet, transient_retry

OWID_BLOOM_URL = (
    "https://ourworldindata.org/grapher/"
    "date-of-the-peak-cherry-tree-blossom-in-kyoto.csv"
)
NOAA_TEMP_URL = (
    "https://www.ncei.noaa.gov/pub/data/paleo/historical/phenology/japan/"
    "kyoto2010temp.txt"
)
NOAA_MISSING = -999.9  # sentinel for missing values in the NOAA text files

BLOOM_SCHEMA = pa.schema([
    ("year", pa.int64()),
    ("day_of_year", pa.int64()),
    ("thirty_year_average", pa.float64()),  # nullable: blank in early/sparse years
])

TEMP_SCHEMA = pa.schema([
    ("year", pa.int64()),
    ("temp_reconstructed", pa.float64()),  # nullable: missing where not reconstructed
    ("temp_observed", pa.float64()),       # nullable: missing before instrumental record
])


@transient_retry()
def _fetch_text(url: str) -> str:
    resp = get(url, timeout=(10.0, 120.0))
    resp.raise_for_status()
    return resp.text


def fetch_bloom_dates(node_id: str) -> None:
    """OWID peak-bloom CSV → parquet. Columns: Entity,Code,Year,
    'Day of the year with peak cherry blossom','Thirty-year average'."""
    asset = node_id
    text = _fetch_text(OWID_BLOOM_URL)
    reader = csv.DictReader(io.StringIO(text))
    years, days, avgs = [], [], []
    for row in reader:
        day = row.get("Day of the year with peak cherry blossom", "").strip()
        if not day:
            continue  # no bloom observation for this year — drop
        years.append(int(row["Year"]))
        days.append(int(day))
        avg = row.get("Thirty-year average", "").strip()
        avgs.append(float(avg) if avg else None)
    table = pa.table(
        {"year": years, "day_of_year": days, "thirty_year_average": avgs},
        schema=BLOOM_SCHEMA,
    )
    save_raw_parquet(table, asset)


def fetch_temperature_reconstruction(node_id: str) -> None:
    """NOAA kyoto2010temp.txt → parquet. Tab-separated; a '#'-commented header
    precedes a 'age_CE\ttemprec\ttempobs' column row then data lines. -999.9 is
    the missing sentinel for both temperature columns."""
    asset = node_id
    text = _fetch_text(NOAA_TEMP_URL)
    years, recs, obss = [], [], []
    seen_header = False
    for line in text.splitlines():
        if line.startswith("#") or not line.strip():
            continue
        parts = line.split("\t")
        if not seen_header:
            # the first non-comment line is the column header row
            if parts[0].strip() == "age_CE":
                seen_header = True
            continue
        if len(parts) < 3:
            continue
        year = int(parts[0].strip())
        rec = float(parts[1].strip())
        obs = float(parts[2].strip())
        years.append(year)
        recs.append(None if rec == NOAA_MISSING else rec)
        obss.append(None if obs == NOAA_MISSING else obs)
    table = pa.table(
        {"year": years, "temp_reconstructed": recs, "temp_observed": obss},
        schema=TEMP_SCHEMA,
    )
    save_raw_parquet(table, asset)


DOWNLOAD_SPECS = [
    NodeSpec(
        id="kyoto-cherry-blossom-bloom-dates",
        fn=fetch_bloom_dates,
        kind="download",
    ),
    NodeSpec(
        id="kyoto-cherry-blossom-temperature-reconstruction",
        fn=fetch_temperature_reconstruction,
        kind="download",
    ),
]
