"""UN Population Division — World Population Prospects 2024 (Standard projections).

Mechanism: bulk_csv. Each subset is one or more stable, public, gzipped CSV
files under the WPP2024 "Standard projections / CSV" directory. There is no
auth and no incremental filter (the REST /data endpoint is Bearer-gated), so
this is a stateless full re-pull: every run downloads the whole corpus and
overwrites. Files are streamed (decompress -> pyarrow CSV reader -> parquet
writer) so memory stays bounded even for the multi-hundred-MB life-table files.

Per-subset notes on the file layout:
  * Projection variant (Medium/High/Low/...) is the `Variant` column; we publish
    only the Medium variant, the standard projection.
  * Age-detailed groups are split by the source into 1950-2023 (estimates) and
    2024-2100 (projections) files with identical schemas — concatenated here.
  * Complete life tables are additionally split into Both/Male/Female files
    (each carries the `Sex` column: Total/Male/Female) — also concatenated.
  * Population/fertility values are in thousands, per the WPP convention.
"""

import io
import gzip

import pyarrow as pa
import pyarrow.csv as pacsv

from subsets_utils import (
    NodeSpec,
    SqlNodeSpec,
    get,
    raw_parquet_writer,
    transient_retry,
)

SLUG = "un-population-division"
BASE = "https://population.un.org/wpp/assets/Excel%20Files/1_Indicator%20(Standard)/CSV_FILES"

# --- schemas (explicit; pinned via column_names + column_types) --------------
# Column names come straight from the CSV header order; we declare them so the
# UTF-8 BOM on the header row never leaks into a field name (we skip the header
# row and supply names ourselves), and so every streamed batch conforms.

_f = pa.float64()
_i = pa.int64()
_s = pa.string()

_PREFIX = [
    ("SortOrder", _i), ("LocID", _i), ("Notes", _s), ("ISO3_code", _s),
    ("ISO2_code", _s), ("SDMX_code", _s), ("LocTypeID", _i), ("LocTypeName", _s),
    ("ParentID", _i), ("Location", _s), ("VarID", _i), ("Variant", _s), ("Time", _i),
]
_AGE_DIM = [
    ("MidPeriod", _f), ("AgeGrp", _s), ("AgeGrpStart", _i), ("AgeGrpSpan", _i),
]
_LIFE_DIM = [
    ("MidPeriod", _f), ("SexID", _i), ("Sex", _s),
    ("AgeGrp", _s), ("AgeGrpStart", _i), ("AgeGrpSpan", _i),
]

_DEMO_MEASURES = [
    "TPopulation1Jan", "TPopulation1July", "TPopulationMale1July", "TPopulationFemale1July",
    "PopDensity", "PopSexRatio", "MedianAgePop", "NatChange", "NatChangeRT", "PopChange",
    "PopGrowthRate", "DoublingTime", "Births", "Births1519", "CBR", "TFR", "NRR", "MAC",
    "SRB", "Deaths", "DeathsMale", "DeathsFemale", "CDR", "LEx", "LExMale", "LExFemale",
    "LE15", "LE15Male", "LE15Female", "LE65", "LE65Male", "LE65Female", "LE80", "LE80Male",
    "LE80Female", "InfantDeaths", "IMR", "LBsurvivingAge1", "Under5Deaths", "Q5", "Q0040",
    "Q0040Male", "Q0040Female", "Q0060", "Q0060Male", "Q0060Female", "Q1550", "Q1550Male",
    "Q1550Female", "Q1560", "Q1560Male", "Q1560Female", "NetMigrations", "CNMR",
]

DEMO_SCHEMA = pa.schema(_PREFIX + [(m, _f) for m in _DEMO_MEASURES])
POP_SCHEMA = pa.schema(_PREFIX + _AGE_DIM + [("PopMale", _f), ("PopFemale", _f), ("PopTotal", _f)])
FERT_SCHEMA = pa.schema(_PREFIX + _AGE_DIM + [("ASFR", _f), ("PASFR", _f), ("Births", _f)])
# Source ships a column literally named "Lx"; renamed to "nLx" here so it does
# not collide (case-insensitively) with "lx" once DuckDB reads the parquet.
_LIFE_MEASURES = ["mx", "qx", "px", "lx", "dx", "nLx", "Sx", "Tx", "ex", "ax"]
LIFE_SCHEMA = pa.schema(_PREFIX + _LIFE_DIM + [(m, _f) for m in _LIFE_MEASURES])

# --- entity -> (shape, schema, source files) ---------------------------------
# `shape` selects the transform SQL template below.

ENTITY_SPECS = {
    "demographic-indicators": (
        "demo", DEMO_SCHEMA,
        ["WPP2024_Demographic_Indicators_Medium.csv.gz"],
    ),
    "population-1january-by-age5-sex": (
        "pop", POP_SCHEMA,
        ["WPP2024_Population1JanuaryByAge5GroupSex_Medium.csv.gz"],
    ),
    "population-1july-by-age5-sex": (
        "pop", POP_SCHEMA,
        ["WPP2024_PopulationByAge5GroupSex_Medium.csv.gz"],
    ),
    "population-1january-by-single-age-sex": (
        "pop", POP_SCHEMA,
        ["WPP2024_Population1JanuaryBySingleAgeSex_Medium_1950-2023.csv.gz",
         "WPP2024_Population1JanuaryBySingleAgeSex_Medium_2024-2100.csv.gz"],
    ),
    "population-1july-by-single-age-sex": (
        "pop", POP_SCHEMA,
        ["WPP2024_PopulationBySingleAgeSex_Medium_1950-2023.csv.gz",
         "WPP2024_PopulationBySingleAgeSex_Medium_2024-2100.csv.gz"],
    ),
    "fertility-by-age5": (
        "fert", FERT_SCHEMA,
        ["WPP2024_Fertility_by_Age5.csv.gz"],
    ),
    "fertility-by-age1": (
        "fert", FERT_SCHEMA,
        ["WPP2024_Fertility_by_Age1.csv.gz"],
    ),
    "life-table-abridged": (
        "life", LIFE_SCHEMA,
        ["WPP2024_Life_Table_Abridged_Medium_1950-2023.csv.gz",
         "WPP2024_Life_Table_Abridged_Medium_2024-2100.csv.gz"],
    ),
    "life-table-complete": (
        "life", LIFE_SCHEMA,
        ["WPP2024_Life_Table_Complete_Medium_Both_1950-2023.csv.gz",
         "WPP2024_Life_Table_Complete_Medium_Both_2024-2100.csv.gz",
         "WPP2024_Life_Table_Complete_Medium_Male_1950-2023.csv.gz",
         "WPP2024_Life_Table_Complete_Medium_Male_2024-2100.csv.gz",
         "WPP2024_Life_Table_Complete_Medium_Female_1950-2023.csv.gz",
         "WPP2024_Life_Table_Complete_Medium_Female_2024-2100.csv.gz"],
    ),
}

ENTITY_IDS = list(ENTITY_SPECS)


# --- download ----------------------------------------------------------------


@transient_retry()
def _download(url: str) -> bytes:
    resp = get(url, timeout=(10.0, 300.0))
    resp.raise_for_status()
    return resp.content


def fetch_one(node_id: str) -> None:
    """Stream every source CSV for this subset into one raw parquet asset."""
    asset = node_id  # the spec id IS the asset name
    entity = node_id[len(SLUG) + 1:]
    _shape, schema, files = ENTITY_SPECS[entity]

    read_opts = pacsv.ReadOptions(
        column_names=schema.names, skip_rows=1, block_size=32 << 20,
    )
    convert_opts = pacsv.ConvertOptions(column_types=schema)

    total = 0
    with raw_parquet_writer(asset, schema) as writer:
        for fname in files:
            content = _download(f"{BASE}/{fname}")
            stream = gzip.GzipFile(fileobj=io.BytesIO(content))
            reader = pacsv.open_csv(stream, read_options=read_opts, convert_options=convert_opts)
            for batch in reader:
                if batch.num_rows:
                    writer.write_batch(batch)
                    total += batch.num_rows
    if total == 0:
        raise AssertionError(f"{asset}: parsed 0 rows from {files} - source layout may have changed")


DOWNLOAD_SPECS = [
    NodeSpec(id=f"{SLUG}-{eid}", fn=fetch_one, kind="download")
    for eid in ENTITY_IDS
]


# --- transform ---------------------------------------------------------------
# Thin parse/rename/type pass: standardise the location/time identity columns
# and carry every measure column through unchanged (`* EXCLUDE`). MidPeriod is
# dropped (redundant with Time); SexID dropped in favour of the Sex label.
#
# We publish only the Medium (standard) projection. Most files are already
# Medium-only by filename, but the fertility CSVs bundle all 18 projection
# variants in one file, so the `Variant = 'Medium'` filter below is what keeps
# every published table on the standard projection (a no-op for the rest).
_MEDIUM = "Variant = 'Medium'"

_DROP_COMMON = (
    "SortOrder, LocID, Notes, ISO3_code, ISO2_code, SDMX_code, LocTypeID, "
    "LocTypeName, ParentID, Location, VarID, Variant, Time"
)
_IDENTITY = (
    'LocID AS location_id, Location AS location_name, ISO3_code AS iso3, '
    'LocTypeName AS location_type, ParentID AS parent_id, Variant AS variant, '
    'Time AS year'
)


def _transform_sql(shape: str, dep: str) -> str:
    if shape == "demo":
        return (
            f'SELECT {_IDENTITY}, * EXCLUDE ({_DROP_COMMON}) '
            f'FROM "{dep}" WHERE LocID IS NOT NULL AND {_MEDIUM}'
        )
    if shape in ("pop", "fert"):
        return (
            f'SELECT {_IDENTITY}, * EXCLUDE ({_DROP_COMMON}, MidPeriod) '
            f'FROM "{dep}" WHERE LocID IS NOT NULL AND {_MEDIUM}'
        )
    # life
    return (
        f'SELECT {_IDENTITY}, Sex AS sex, '
        f'* EXCLUDE ({_DROP_COMMON}, MidPeriod, SexID, Sex) '
        f'FROM "{dep}" WHERE LocID IS NOT NULL AND {_MEDIUM}'
    )


TRANSFORM_SPECS = [
    SqlNodeSpec(
        id=f"{SLUG}-{eid}-transform",
        deps=[f"{SLUG}-{eid}"],
        sql=_transform_sql(ENTITY_SPECS[eid][0], f"{SLUG}-{eid}"),
    )
    for eid in ENTITY_IDS
]
