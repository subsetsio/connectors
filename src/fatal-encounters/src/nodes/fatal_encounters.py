"""Fatal Encounters connector.

Single-dataset source: the entire database is one public Google Sheet, exported
as CSV in one request (~31.5k rows, ~26 MB). Stateless full re-pull every run —
the source updates the sheet continuously and there is no incremental filter, so
we re-fetch the whole corpus and overwrite. Raw is parsed to a clean,
snake_cased, all-string parquet (the sheet carries formula-helper and internal
"temp" columns we drop); the transform does the typing.
"""

import csv
import io
from datetime import datetime

import pyarrow as pa
from subsets_utils import NodeSpec, get, save_raw_parquet

CSV_URL = (
    "https://docs.google.com/spreadsheets/d/"
    "1dKmaV_JiWcG8XBoRgP8b4e9Eopkpgt7FL7nyspvzAsE/export?format=csv&gid=0"
)

# Stripped source header -> output column name. Only these columns are kept;
# the sheet's "Temporary"/"Temp" working columns, the INTERNAL-USE dispositions
# column, the blank spacer columns, and the formula/redundant id columns are
# intentionally dropped. Raw stays all-string; the transform casts.
COLUMN_MAP = {
    "Unique ID": "unique_id",
    "Name": "name",
    "Age": "age",
    "Gender": "gender",
    "Race": "race",
    "Race with imputations": "race_with_imputations",
    "Imputation probability": "imputation_probability",
    "URL of image (PLS NO HOTLINKS)": "image_url",
    "Date of injury resulting in death (month/day/year)": "date_of_death",
    "Location of injury (address)": "location_address",
    "Location of death (city)": "city",
    "State": "state",
    "Location of death (zip code)": "zip_code",
    "Location of death (county)": "county",
    "Full Address": "full_address",
    "Latitude": "latitude",
    "Longitude": "longitude",
    "Agency or agencies involved": "agency",
    "Highest level of force": "highest_level_of_force",
    "Armed/Unarmed": "armed_unarmed",
    "Alleged weapon": "alleged_weapon",
    "Aggressive physical movement": "aggressive_physical_movement",
    "Fleeing/Not fleeing": "fleeing",
    "Brief description": "brief_description",
    "Intended use of force (Developing)": "intended_use_of_force",
    "Supporting document link": "supporting_document_link",
}

SCHEMA = pa.schema([(name, pa.string()) for name in COLUMN_MAP.values()])


def _fetch_csv(url: str) -> bytes:
    resp = get(url, timeout=(10.0, 180.0))
    resp.raise_for_status()
    return resp.content


def _normalize_date(value: str | None) -> str | None:
    if not value:
        return None
    value = value.strip()
    for fmt in ("%m/%d/%Y", "%m/%d/%y"):
        try:
            return datetime.strptime(value, fmt).date().isoformat()
        except ValueError:
            pass
    return None


def fetch_fatal_encounters(node_id: str) -> None:
    asset = node_id  # the runtime passes the spec id; it IS the asset name
    text = _fetch_csv(CSV_URL).decode("utf-8-sig")
    reader = csv.reader(io.StringIO(text))

    header = [h.strip() for h in next(reader)]
    idx = {}
    for src, out in COLUMN_MAP.items():
        if src not in header:
            raise AssertionError(f"expected column {src!r} not found in CSV header")
        idx[out] = header.index(src)

    uid_pos = idx["unique_id"]
    cols = {out: [] for out in COLUMN_MAP.values()}
    for row in reader:
        # Skip fully-blank trailer rows and rows without a unique id (the sheet
        # has a handful of formula/spacer artifacts that carry no record).
        if uid_pos >= len(row) or not row[uid_pos].strip():
            continue
        for out, pos in idx.items():
            val = row[pos].strip() if pos < len(row) else ""
            if out == "date_of_death":
                val = _normalize_date(val)
            cols[out].append(val if val else None)

    table = pa.table(
        {name: pa.array(cols[name], type=pa.string()) for name in COLUMN_MAP.values()},
        schema=SCHEMA,
    )
    save_raw_parquet(table, asset)


DOWNLOAD_SPECS = [
    NodeSpec(
        id="fatal-encounters-fatal-encounters",
        fn=fetch_fatal_encounters,
        kind="download",
    ),
]
