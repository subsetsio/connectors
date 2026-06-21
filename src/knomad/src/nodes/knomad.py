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
    SqlNodeSpec,
    get,
    save_raw_parquet,
    transient_retry,
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


@transient_retry()
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


# --- transforms: one published Delta table per subset ---------------------

# 2D flow indicators (MRI, MRO): country x year time series.
def _flow_sql(dep: str) -> str:
    return f'''
        SELECT
            REF_AREA                            AS country_code,
            REF_AREA_LABEL                      AS country,
            CAST(TIME_PERIOD AS INTEGER)        AS year,
            TRY_CAST(OBS_VALUE AS DOUBLE)       AS value_usd_million,
            UNIT_MEASURE_LABEL                  AS unit,
            INDICATOR_LABEL                     AS indicator,
            OBS_STATUS                          AS obs_status
        FROM "{dep}"
        WHERE OBS_VALUE IS NOT NULL
          AND TRY_CAST(OBS_VALUE AS DOUBLE) IS NOT NULL
          AND TRY_CAST(TIME_PERIOD AS INTEGER) IS NOT NULL
    '''


# 3D bilateral matrices (BRE, MIG): origin x destination corridor.
# REF_AREA is the indicator's primary country; COMP_BREAKDOWN_1 carries the
# counterpart country, code-prefixed 'WB_KNOMAD_' (stripped here to ISO3).
def _bilateral_sql(dep: str, value_col: str) -> str:
    return f'''
        SELECT
            REF_AREA                                          AS country_code,
            REF_AREA_LABEL                                    AS country,
            REPLACE(COMP_BREAKDOWN_1, 'WB_KNOMAD_', '')       AS counterpart_code,
            COMP_BREAKDOWN_1_LABEL                            AS counterpart,
            CAST(TIME_PERIOD AS INTEGER)                      AS year,
            TRY_CAST(OBS_VALUE AS DOUBLE)                     AS {value_col},
            UNIT_MEASURE_LABEL                                AS unit,
            INDICATOR_LABEL                                   AS indicator,
            OBS_STATUS                                        AS obs_status
        FROM "{dep}"
        WHERE OBS_VALUE IS NOT NULL
          AND TRY_CAST(OBS_VALUE AS DOUBLE) IS NOT NULL
          AND COMP_BREAKDOWN_1 NOT IN ('_T', '_Z')
          AND TRY_CAST(TIME_PERIOD AS INTEGER) IS NOT NULL
    '''


TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="knomad-wb-knomad-mri-transform",
        deps=["knomad-wb-knomad-mri"],
        sql=_flow_sql("knomad-wb-knomad-mri"),
    ),
    SqlNodeSpec(
        id="knomad-wb-knomad-mro-transform",
        deps=["knomad-wb-knomad-mro"],
        sql=_flow_sql("knomad-wb-knomad-mro"),
    ),
    SqlNodeSpec(
        id="knomad-wb-knomad-bre-transform",
        deps=["knomad-wb-knomad-bre"],
        sql=_bilateral_sql("knomad-wb-knomad-bre", "remittance_usd_million"),
    ),
    SqlNodeSpec(
        id="knomad-wb-knomad-mig-transform",
        deps=["knomad-wb-knomad-mig"],
        sql=_bilateral_sql("knomad-wb-knomad-mig", "migrant_stock"),
    ),
]
