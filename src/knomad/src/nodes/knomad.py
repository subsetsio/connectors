"""KNOMAD (World Bank Data360 database WB_KNOMAD) connector.

Source: the Global Knowledge Partnership on Migration and Development, now hosted
on World Bank Data360 under database id WB_KNOMAD. Exactly four indicators, each
published as its own bulk CSV at a stable URL:

  WB_KNOMAD_MRI  Remittance inflows (US$ million)      country x year (2000-)
  WB_KNOMAD_MRO  Remittance outflows (US$ million)     country x year (2000-)
  WB_KNOMAD_BRE  Bilateral Remittance Estimates        origin x destination, 2021
  WB_KNOMAD_MIG  Bilateral Estimate of Migrant Stocks  origin x destination, 2021

Fetch shape: stateless full re-pull. Each CSV is 2-7MB and fully self-describing
(SDMX-flat: REF_AREA, TIME_PERIOD, OBS_VALUE, plus *_LABEL columns; bilateral
indicators carry the counterpart country in COMP_BREAKDOWN_1, code-prefixed
'WB_KNOMAD_'). We re-fetch the whole corpus every run and overwrite — no
watermark/cursor (the source exposes no incremental filter and the corpus is
tiny). Raw is saved as parquet with an explicit all-string schema; the transform
SQL casts and reshapes.
"""

import csv
import io

import pyarrow as pa
from subsets_utils import (
    NodeSpec,
    get,
    save_raw_parquet,
)

CSV_URL = "https://data360files.worldbank.org/data360-data/data/WB_KNOMAD/{indicator}.csv"

# Columns kept from the SDMX-flat CSV. All carried through as strings; the
# transform SQL does the typing. Stable across all four indicator files.
KEEP = [
    "INDICATOR",
    "INDICATOR_LABEL",
    "REF_AREA",
    "REF_AREA_LABEL",
    "COMP_BREAKDOWN_1",
    "COMP_BREAKDOWN_1_LABEL",
    "TIME_PERIOD",
    "OBS_VALUE",
    "UNIT_MEASURE",
    "UNIT_MEASURE_LABEL",
    "FREQ_LABEL",
    "OBS_STATUS",
]

SCHEMA = pa.schema([(c, pa.string()) for c in KEEP])


def _indicator_from_node_id(node_id: str) -> str:
    """'knomad-wb-knomad-mri' -> 'WB_KNOMAD_MRI'."""
    return node_id[len("knomad-"):].upper().replace("-", "_")


def _fetch_csv(url: str) -> str:
    resp = get(url, timeout=(10.0, 120.0))
    resp.raise_for_status()
    return resp.text


def fetch_one(node_id: str) -> None:
    asset = node_id
    indicator = _indicator_from_node_id(node_id)
    text = _fetch_csv(CSV_URL.format(indicator=indicator))

    reader = csv.DictReader(io.StringIO(text))
    cols = {c: [] for c in KEEP}
    n = 0
    for row in reader:
        for c in KEEP:
            v = row.get(c)
            cols[c].append(v if v not in ("", None) else None)
        n += 1
    if n == 0:
        raise AssertionError(f"{indicator}: bulk CSV returned zero data rows")

    table = pa.table({c: pa.array(cols[c], type=pa.string()) for c in KEEP}, schema=SCHEMA)
    save_raw_parquet(table, asset)


DOWNLOAD_SPECS = [
    NodeSpec(id="knomad-wb-knomad-mri", fn=fetch_one, kind="download"),
    NodeSpec(id="knomad-wb-knomad-mro", fn=fetch_one, kind="download"),
    NodeSpec(id="knomad-wb-knomad-bre", fn=fetch_one, kind="download"),
    NodeSpec(id="knomad-wb-knomad-mig", fn=fetch_one, kind="download"),
]
