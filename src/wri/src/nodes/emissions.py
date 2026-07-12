"""WRI historical emissions — country GHG emissions, 1850-2024.

The source CSV is WIDE (one column per year); we unpivot to long form
(year, value) here so the transform stays a thin cast pass.
"""

import csv

import pyarrow as pa

from subsets_utils import raw_parquet_writer
from utils import download_zip, open_member

_EMISSIONS_SCHEMA = pa.schema([
    ("iso_code3", pa.string()),
    ("country", pa.string()),
    ("data_source", pa.string()),
    ("sector", pa.string()),
    ("gas", pa.string()),
    ("unit", pa.string()),
    ("year", pa.int16()),
    ("value", pa.float64()),
])
_BATCH_ROWS = 200_000


def fetch_emissions(node_id: str) -> None:
    """historical_emissions: unpivot the wide year columns into long rows and
    stream to parquet in bounded batches (the long form is a few million rows)."""
    asset = node_id  # the spec id IS the asset name
    content = download_zip("historical_emissions")
    reader = csv.reader(open_member(content, "historical_emissions.csv"))
    header = next(reader)
    # First 6 columns are metadata; the remainder are year columns.
    meta_cols = header[:6]
    assert [c.lower() for c in meta_cols] == [
        "iso", "country", "data source", "sector", "gas", "unit"
    ], f"unexpected emissions header: {meta_cols}"
    year_cols = header[6:]
    years = [int(y) for y in year_cols]  # raises if a non-year column appears

    cols = {name: [] for name in _EMISSIONS_SCHEMA.names}
    n_written = 0

    def _flush(writer):
        nonlocal cols
        if not cols["year"]:
            return
        table = pa.table({k: pa.array(v) for k, v in cols.items()},
                         schema=_EMISSIONS_SCHEMA)
        writer.write_table(table)
        cols = {name: [] for name in _EMISSIONS_SCHEMA.names}

    with raw_parquet_writer(asset, _EMISSIONS_SCHEMA) as writer:
        for row in reader:
            iso, country, data_source, sector, gas, unit = row[:6]
            for year, raw_val in zip(years, row[6:]):
                if raw_val == "" or raw_val is None:
                    continue
                try:
                    value = float(raw_val)
                except ValueError:
                    continue  # non-numeric cell (e.g. 'N/A'); drop it
                cols["iso_code3"].append(iso)
                cols["country"].append(country)
                cols["data_source"].append(data_source)
                cols["sector"].append(sector)
                cols["gas"].append(gas)
                cols["unit"].append(unit)
                cols["year"].append(year)
                cols["value"].append(value)
            if len(cols["year"]) >= _BATCH_ROWS:
                n_written += len(cols["year"])
                _flush(writer)
        n_written += len(cols["year"])
        _flush(writer)

    assert n_written > 0, "historical_emissions produced 0 long rows"
