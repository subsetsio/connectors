"""Wittgenstein Centre Human Capital Data Explorer (WIC Population & Human
Capital Projections 2023, Data Explorer v3.0).

Source: Zenodo record 14718294 (DOI 10.5281/zenodo.14718294), Open Access.
The whole corpus is a fixed set of release CSVs, one HTTP GET each. There is no
incremental query and no per-country API — every file is the full corpus for
its indicator, so this is a stateless full re-pull every refresh (the maintain
step decides whether a refresh runs). A new projection round publishes a new
Zenodo record/DOI; bump _RECORD when that happens.

Seven detailed projection files (one per SSP scenario) share one schema and are
unioned into a single `projection-results` raw asset with `scenario` added as a
column. The smaller indicator files (ASFR, EDUprop, MYS, SX, SRB) carry every
scenario as side-by-side columns; they are stored verbatim and unpivoted to a
tidy `scenario` column in the transform.

Region and education codes (reg100, e1..e6) are decoded to human-readable
`region_name` / `edu_label` columns *at download time*, by fetching the small
recode dictionary and mapping in-memory. This is done here (not via a SQL join
in the transform) so that every transform depends only on its own raw asset —
a shared raw dependency read concurrently by many transforms is fragile under
the object-store LIST that resolves dep globs. The recode dictionary is also
stored as its own asset and published as a standalone lookup table.
"""

import io

import pyarrow as pa
import pyarrow.csv as pacsv

from subsets_utils import (
    NodeSpec,
    SqlNodeSpec,
    get,
    transient_retry,
    save_raw_parquet,
    raw_parquet_writer,
)

_RECORD = "https://zenodo.org/api/records/14718294"
_RECODE_FILE = "Recode dictionary.csv"

_SCENARIO_COLS = ["SSP1", "SSP2", "SSP2mig0", "SSP2mig2x", "SSP3", "SSP4", "SSP5"]

# Coercion contract applied at CSV parse time. pyarrow applies these to columns
# that are present and infers the rest (recode's var/varnm/... -> string; entries
# for columns a given file lacks are ignored).
_COLUMN_TYPES = {
    "region": pa.string(),
    "Time": pa.int64(),
    "sex": pa.string(),
    "edu": pa.string(),
    "agest": pa.int64(),
    **{c: pa.float64() for c in _SCENARIO_COLS},
}

# Simple one-file-per-asset downloads (filename on the Zenodo record).
_SIMPLE_FILES = {
    "wittgenstein-centre-asfr": "ASFR_AE_SSPs_V14.csv",
    "wittgenstein-centre-edu-proportions": "EDUprop_AGE_SSPs_V14.csv",
    "wittgenstein-centre-mean-years-schooling": "MYS_AG_SSPs_V14.csv",
    "wittgenstein-centre-sex-ratio-at-birth": "SRB_SSPs_V14.csv",
    "wittgenstein-centre-survival-ratios": "SX_AGE_SSPs_V14.csv",
    "wittgenstein-centre-recode-dictionary": _RECODE_FILE,
}

# The 7 detailed projection files -> their scenario label, unioned into one asset.
_PROJ_FILES = {
    "PROJresult_AGE_SSP1_V14.csv": "SSP1",
    "PROJresult_AGE_SSP2_V14.csv": "SSP2",
    "PROJresult_AGE_SSP2mig0_V14.csv": "SSP2mig0",
    "PROJresult_AGE_SSP2mig2x_V14.csv": "SSP2mig2x",
    "PROJresult_AGE_SSP3_V14.csv": "SSP3",
    "PROJresult_AGE_SSP4_V14.csv": "SSP4",
    "PROJresult_AGE_SSP5_V14.csv": "SSP5",
}

_PROJ_SCHEMA = pa.schema([
    ("region", pa.string()),
    ("region_name", pa.string()),
    ("Time", pa.int64()),
    ("sex", pa.string()),
    ("edu", pa.string()),
    ("edu_label", pa.string()),
    ("agest", pa.int64()),
    ("pop", pa.float64()),
    ("births", pa.float64()),
    ("emi", pa.float64()),
    ("imm", pa.float64()),
    ("deaths", pa.float64()),
    ("scenario", pa.string()),
])


@transient_retry()
def _fetch_csv_bytes(filename: str) -> bytes:
    # Zenodo file endpoint; spaces in filenames must be %20-encoded.
    url = f"{_RECORD}/files/{filename.replace(' ', '%20')}/content"
    resp = get(url, timeout=(10.0, 300.0))
    resp.raise_for_status()
    return resp.content


def _read_csv(content: bytes) -> pa.Table:
    convert = pacsv.ConvertOptions(column_types=_COLUMN_TYPES)
    return pacsv.read_csv(io.BytesIO(content), convert_options=convert)


def _recode_maps() -> tuple[dict, dict]:
    """(region code -> name, edu code -> label) from the recode dictionary."""
    table = _read_csv(_fetch_csv_bytes(_RECODE_FILE))
    var = table.column("var").to_pylist()
    val = table.column("varval").to_pylist()
    desc = table.column("varvaldesc").to_pylist()
    region, edu = {}, {}
    for v, code, label in zip(var, val, desc):
        if v == "region":
            region[code] = label
        elif v == "edu":
            edu[code] = label
    return region, edu


def _decode(table: pa.Table, region_map: dict, edu_map: dict) -> pa.Table:
    """Append region_name (and edu_label, when an edu column exists)."""
    regions = table.column("region").to_pylist()
    table = table.append_column(
        "region_name", pa.array([region_map.get(r) for r in regions], pa.string())
    )
    if "edu" in table.column_names:
        edus = table.column("edu").to_pylist()
        table = table.append_column(
            "edu_label", pa.array([edu_map.get(e) for e in edus], pa.string())
        )
    return table


def fetch_simple(node_id: str) -> None:
    """One stable CSV -> one parquet asset. Indicator files get region_name /
    edu_label decoded inline; the recode dictionary is stored verbatim."""
    asset = node_id
    table = _read_csv(_fetch_csv_bytes(_SIMPLE_FILES[node_id]))
    if node_id != "wittgenstein-centre-recode-dictionary":
        region_map, edu_map = _recode_maps()
        table = _decode(table, region_map, edu_map)
    save_raw_parquet(table, asset)


def fetch_projection_results(node_id: str) -> None:
    """Union the 7 per-scenario detailed projection files into one asset, adding
    `scenario` and decoded region_name/edu_label. Streamed one file at a time so
    peak memory is a single ~1.2M-row file, not all 7 at once."""
    asset = node_id
    region_map, edu_map = _recode_maps()
    cols = [f.name for f in _PROJ_SCHEMA]
    with raw_parquet_writer(asset, _PROJ_SCHEMA) as writer:
        for filename, scenario in _PROJ_FILES.items():
            table = _read_csv(_fetch_csv_bytes(filename))
            table = table.append_column(
                "scenario", pa.array([scenario] * table.num_rows, pa.string())
            )
            table = _decode(table, region_map, edu_map)
            # Enforce the declared column order/types before the row-group write.
            table = table.select(cols).cast(_PROJ_SCHEMA)
            writer.write_table(table)


DOWNLOAD_SPECS = [
    NodeSpec(id="wittgenstein-centre-asfr", fn=fetch_simple, kind="download"),
    NodeSpec(id="wittgenstein-centre-edu-proportions", fn=fetch_simple, kind="download"),
    NodeSpec(id="wittgenstein-centre-mean-years-schooling", fn=fetch_simple, kind="download"),
    NodeSpec(id="wittgenstein-centre-sex-ratio-at-birth", fn=fetch_simple, kind="download"),
    NodeSpec(id="wittgenstein-centre-survival-ratios", fn=fetch_simple, kind="download"),
    NodeSpec(id="wittgenstein-centre-recode-dictionary", fn=fetch_simple, kind="download"),
    NodeSpec(id="wittgenstein-centre-projection-results", fn=fetch_projection_results, kind="download"),
]


# --- transforms: one tidy published Delta table per subset -------------------
# Each transform reads ONLY its own raw asset (single dep). Region/edu names are
# already decoded in the raw, so transforms stay a thin cast/unpivot pass.

_UNPIVOT_ON = ", ".join(_SCENARIO_COLS)


def _indicator_sql(dep: str, value_name: str, *, has_edu: bool) -> str:
    """Unpivot a wide indicator asset to (..., scenario, <value_name>)."""
    edu_select = "edu, edu_label," if has_edu else ""
    return f"""
        WITH long AS (
            UNPIVOT "{dep}" ON {_UNPIVOT_ON} INTO NAME scenario VALUE value
        )
        SELECT
            region,
            region_name,
            CAST(Time AS INTEGER) AS year,
            sex,
            {edu_select}
            CAST(agest AS INTEGER) AS age_start,
            scenario,
            CAST(value AS DOUBLE) AS {value_name}
        FROM long
        WHERE value IS NOT NULL
    """


_SRB_SQL = f"""
    WITH long AS (
        UNPIVOT "wittgenstein-centre-sex-ratio-at-birth" ON {_UNPIVOT_ON}
        INTO NAME scenario VALUE value
    )
    SELECT
        region,
        region_name,
        CAST(Time AS INTEGER) AS year,
        scenario,
        CAST(value AS DOUBLE) AS sex_ratio_at_birth
    FROM long
    WHERE value IS NOT NULL
"""

_PROJ_SQL = """
    SELECT
        region,
        region_name,
        CAST(Time AS INTEGER) AS year,
        sex,
        edu,
        edu_label,
        CAST(agest AS INTEGER) AS age_start,
        scenario,
        CAST(pop AS DOUBLE) AS population,
        CAST(births AS DOUBLE) AS births,
        CAST(emi AS DOUBLE) AS emigrants,
        CAST(imm AS DOUBLE) AS immigrants,
        CAST(deaths AS DOUBLE) AS deaths
    FROM "wittgenstein-centre-projection-results"
"""

_RECODE_SQL = """
    SELECT
        var AS variable,
        varnm AS variable_label,
        varval AS code,
        varvaldesc AS description
    FROM "wittgenstein-centre-recode-dictionary"
    WHERE var IS NOT NULL
"""

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="wittgenstein-centre-asfr-transform",
        deps=["wittgenstein-centre-asfr"],
        sql=_indicator_sql("wittgenstein-centre-asfr", "asfr_births_per_1000_women", has_edu=True),
    ),
    SqlNodeSpec(
        id="wittgenstein-centre-edu-proportions-transform",
        deps=["wittgenstein-centre-edu-proportions"],
        sql=_indicator_sql("wittgenstein-centre-edu-proportions", "proportion", has_edu=True),
    ),
    SqlNodeSpec(
        id="wittgenstein-centre-mean-years-schooling-transform",
        deps=["wittgenstein-centre-mean-years-schooling"],
        sql=_indicator_sql("wittgenstein-centre-mean-years-schooling", "mean_years_schooling", has_edu=False),
    ),
    SqlNodeSpec(
        id="wittgenstein-centre-survival-ratios-transform",
        deps=["wittgenstein-centre-survival-ratios"],
        sql=_indicator_sql("wittgenstein-centre-survival-ratios", "survival_ratio", has_edu=True),
    ),
    SqlNodeSpec(
        id="wittgenstein-centre-sex-ratio-at-birth-transform",
        deps=["wittgenstein-centre-sex-ratio-at-birth"],
        sql=_SRB_SQL,
    ),
    SqlNodeSpec(
        id="wittgenstein-centre-projection-results-transform",
        deps=["wittgenstein-centre-projection-results"],
        sql=_PROJ_SQL,
    ),
    SqlNodeSpec(
        id="wittgenstein-centre-recode-dictionary-transform",
        deps=["wittgenstein-centre-recode-dictionary"],
        sql=_RECODE_SQL,
    ),
]
