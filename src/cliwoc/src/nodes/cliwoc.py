"""CLIWOC — Climatological Database for the World's Oceans, 1750-1854.

A single frozen academic archive (release 2.1): ~287k daily weather
observations abstracted from British, Dutch, French and Spanish naval ship
logbooks. The whole corpus ships as one ~167 MB tab-delimited file at a stable
GitHub-LFS URL, so this is a stateless full re-pull of one asset every refresh
(the data never changes; a refresh is an integrity re-pull, not a delta).

The source file carries 180 legacy IMMA-style columns, most of them sparse. The
download fn parses the TSV and projects the well-grounded, well-populated core:
position, date, ship/voyage provenance, and the descriptive wind/weather text
that is CLIWOC's headline scientific contribution (wind direction & force read
from the logs, in the original language). The instrumental numeric fields
(air/sea temperature, pressure) are deliberately NOT published: their units vary
by nationality and reading instrument across the corpus, so emitting them as
single typed columns would be misleading. The transform is a thin typed
passthrough that publishes one Delta table.
"""

import csv
import datetime as dt
import io

import pyarrow as pa
from subsets_utils import (
    NodeSpec,
    get,
    save_raw_parquet,
    transient_retry,
)

URL = (
    "https://media.githubusercontent.com/media/stvno/stvno.github.io/"
    "master/page/cliwoc/CLIWOC21.tsv"
)

# Explicit schema = the contract for the published core.
SCHEMA = pa.schema(
    [
        ("logbook_id", pa.string()),
        ("record_date", pa.date32()),
        ("year", pa.int32()),
        ("month", pa.int32()),
        ("day", pa.int32()),
        ("latitude", pa.float64()),
        ("longitude", pa.float64()),
        ("ship_name", pa.string()),
        ("nationality", pa.string()),
        ("ship_type", pa.string()),
        ("company", pa.string()),
        ("voyage_from", pa.string()),
        ("voyage_to", pa.string()),
        ("logbook_language", pa.string()),
        ("wind_direction", pa.string()),
        ("wind_force", pa.string()),
        ("weather", pa.string()),
        ("precipitation", pa.string()),
        ("archive_institution", pa.string()),
    ]
)

# published column -> source TSV header name
SOURCE_COLS = {
    "logbook_id": "LogbookIdent",
    "ship_name": "ShipName",
    "nationality": "Nationality",
    "ship_type": "ShipType",
    "company": "Company",
    "voyage_from": "VoyageFrom",
    "voyage_to": "VoyageTo",
    "logbook_language": "LogbookLanguage",
    "wind_direction": "AllWindDirections",
    "wind_force": "AllWindForces",
    "weather": "Weather",
    "precipitation": "PrecipitationDescriptor",
    "archive_institution": "InstName",
}


@transient_retry()
def _download_tsv() -> str:
    resp = get(URL, timeout=(10.0, 300.0))
    resp.raise_for_status()
    # content-type is text/plain with no declared charset; the memo fields carry
    # Dutch/Spanish/French accented text — decode as UTF-8 explicitly.
    return resp.content.decode("utf-8", errors="replace")


def _to_int(v: str):
    v = v.strip()
    if not v:
        return None
    try:
        return int(float(v))
    except ValueError:
        return None


def _to_float(v: str):
    v = v.strip()
    if not v:
        return None
    try:
        return float(v)
    except ValueError:
        return None


def _clean(v: str):
    v = v.strip()
    return v or None


def fetch_observations(node_id: str) -> None:
    asset = node_id  # the spec id IS the asset name

    text = _download_tsv()
    reader = csv.reader(io.StringIO(text), delimiter="\t")
    header = next(reader)
    idx = {name: i for i, name in enumerate(header)}

    def cell(row: list, name: str) -> str:
        i = idx.get(name)
        if i is None or i >= len(row):
            return ""
        return row[i]

    cols: dict[str, list] = {name: [] for name in SCHEMA.names}

    for row in reader:
        year = _to_int(cell(row, "Year"))
        month = _to_int(cell(row, "Month"))
        day = _to_int(cell(row, "Day"))

        record_date = None
        if (
            year is not None
            and month is not None
            and day is not None
            and 1 <= month <= 12
            and 1 <= day <= 31
            and 1600 <= year <= 1900
        ):
            try:
                record_date = dt.date(year, month, day)
            except ValueError:
                record_date = None

        cols["record_date"].append(record_date)
        cols["year"].append(year)
        cols["month"].append(month)
        cols["day"].append(day)
        cols["latitude"].append(_to_float(cell(row, "latitude")))
        cols["longitude"].append(_to_float(cell(row, "longitude")))
        for pub, src in SOURCE_COLS.items():
            cols[pub].append(_clean(cell(row, src)))

    table = pa.table(cols, schema=SCHEMA)
    save_raw_parquet(table, asset)


DOWNLOAD_SPECS = [
    NodeSpec(id="cliwoc-observations", fn=fetch_observations, kind="download"),
]
