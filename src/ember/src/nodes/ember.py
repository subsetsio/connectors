"""Ember electricity data connector.

Source: Ember (ember-energy.org), open CC-BY-4.0 bulk long-format CSVs served as
static files from files.ember-energy.org (GCS-backed). Six published subsets,
one per (geographic-scope x temporal-resolution):

  - global-yearly  : ~215 countries/regions, yearly from 2000
  - global-monthly : ~88 geographies, monthly from 2018
  - europe-yearly  : European countries + EU aggregate, yearly from 1990
  - europe-monthly : European countries + EU aggregate, monthly from 2015
  - us-yearly      : US state-level, yearly
  - us-monthly     : US state-level, monthly

The Europe files share the global files' column list but are a distinct Ember
product rather than a slice of them: they reach a decade further back, and they
disagree with the global file on the value of a few hundred overlapping
(Area, Year, Category, Subcategory, Variable) keys. They are therefore published
as their own tables rather than merged into the global ones.

Each file is one tidy/long table that bundles every metric Ember publishes
(generation, capacity, demand, power-sector emissions, carbon intensity) in the
Category/Subcategory/Variable columns. Unit belongs to the grain rather than
describing it: the same variable is published in several units (generation as
both TWh and % of the mix, emissions as both mtCO2 and gCO2/kWh).

Fetch shape: stateless full re-pull. Each CSV is a full snapshot (~8-105MB, no
incremental query support on the bulk path) re-fetched in full every run and
overwritten. Revisions/late corrections are picked up for free. No watermark,
no cursor.
"""

import io

import pyarrow as pa
import pyarrow.csv as pacsv

from subsets_utils import (
    NodeSpec,
    get,
    save_raw_parquet,
    transient_retry,
)

_BASE = "https://files.ember-energy.org/public-downloads"

ENTITY_URLS = {
    "global-yearly": f"{_BASE}/yearly_full_release_long_format.csv",
    "global-monthly": f"{_BASE}/monthly_full_release_long_format.csv",
    "europe-yearly": f"{_BASE}/europe_yearly_full_release_long_format.csv",
    "europe-monthly": f"{_BASE}/europe_monthly_full_release_long_format.csv",
    "us-yearly": f"{_BASE}/us_yearly_full_release_long_format.csv",
    "us-monthly": f"{_BASE}/us_monthly_full_release_long_format.csv",
}


@transient_retry()
def _download_csv(url: str) -> bytes:
    # Bulk static CSVs; generous read timeout for the ~105MB US monthly file.
    resp = get(url, timeout=(10.0, 600.0))
    resp.raise_for_status()
    return resp.content


def _column_types(is_us: bool, is_monthly: bool) -> dict:
    """Explicit per-column types — the contract that keeps parquet stable across
    refreshes. The period column is the only structural difference between
    yearly (integer Year) and monthly (ISO-date string Date); the geographic
    columns differ between the country-level files (global, Europe) and the
    state-level US files.
    """
    period_col = "Date" if is_monthly else "Year"
    # Monthly periods are ISO first-of-month dates; parse them as real dates so
    # the raw carries the temporal type rather than a string that sorts by luck.
    period_type = pa.date32() if is_monthly else pa.int64()

    if is_us:
        geo = {
            "Country": pa.string(),
            "Country code": pa.string(),
            "State": pa.string(),
            "State code": pa.string(),
            "State type": pa.string(),
        }
    else:
        geo = {
            "Area": pa.string(),
            "ISO 3 code": pa.string(),
            "Area type": pa.string(),
            "Continent": pa.string(),
            "Ember region": pa.string(),
            "EU": pa.float64(),
            "OECD": pa.float64(),
            "G20": pa.float64(),
            "G7": pa.float64(),
            "ASEAN": pa.float64(),
        }

    types = dict(geo)
    types[period_col] = period_type
    types.update(
        {
            "Category": pa.string(),
            "Subcategory": pa.string(),
            "Variable": pa.string(),
            "Unit": pa.string(),
            "Value": pa.float64(),
            "YoY absolute change": pa.float64(),
            "YoY % change": pa.float64(),
        }
    )
    return types


def fetch_one(node_id: str) -> None:
    asset = node_id  # the runtime passes the spec id; it IS the asset name
    entity = node_id[len("ember-"):]
    url = ENTITY_URLS[entity]
    is_us = entity.startswith("us-")
    is_monthly = entity.endswith("-monthly")

    content = _download_csv(url)

    table = pacsv.read_csv(
        io.BytesIO(content),
        read_options=pacsv.ReadOptions(use_threads=True),
        convert_options=pacsv.ConvertOptions(
            column_types=_column_types(is_us, is_monthly),
            strings_can_be_null=True,
        ),
    )
    save_raw_parquet(table, asset)


DOWNLOAD_SPECS = [
    NodeSpec(id=f"ember-{entity}", fn=fetch_one, kind="download")
    for entity in ENTITY_URLS
]
