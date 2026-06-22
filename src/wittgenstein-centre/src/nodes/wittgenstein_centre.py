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
tidy `scenario` column in the transform. The recode dictionary is stored as-is
and used both as its own published lookup and to decode region/education codes
in the other transforms.
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

_SCENARIO_COLS = ["SSP1", "SSP2", "SSP2mig0", "SSP2mig2x", "SSP3", "SSP4", "SSP5"]

# Coercion contract applied at CSV parse time. pyarrow uses these for columns
# that are present and infers the rest (e.g. recode's var/varnm/... -> string).
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
    "wittgenstein-centre-recode-dictionary": "Recode dictionary.csv",
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
    ("Time", pa.int64()),
    ("sex", pa.string()),
    ("edu", pa.string()),
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


def fetch_simple(node_id: str) -> None:
    """One stable CSV -> one parquet asset, stored verbatim."""
    asset = node_id
    filename = _SIMPLE_FILES[node_id]
    table = _read_csv(_fetch_csv_bytes(filename))
    save_raw_parquet(table, asset)


def fetch_projection_results(node_id: str) -> None:
    """Union the 7 per-scenario detailed projection files into one asset,
    adding a `scenario` column. Streamed one file at a time so peak memory is
    a single ~1.2M-row file, not all 7 at once."""
    asset = node_id
    with raw_parquet_writer(asset, _PROJ_SCHEMA) as writer:
        for filename, scenario in _PROJ_FILES.items():
            table = _read_csv(_fetch_csv_bytes(filename))
            table = table.append_column(
                "scenario", pa.array([scenario] * table.num_rows, pa.string())
            )
            # Enforce the declared column order/types before the row-group write.
            table = table.select([f.name for f in _PROJ_SCHEMA]).cast(_PROJ_SCHEMA)
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

_RECODE = "wittgenstein-centre-recode-dictionary"
# Region/education code decoders, reused across indicator transforms.
_REG_CTE = (
    f"reg AS (SELECT varval AS region, varvaldesc AS region_name "
    f"FROM \"{_RECODE}\" WHERE var = 'region')"
)
_EDU_CTE = (
    f"edu AS (SELECT varval AS edu, varvaldesc AS edu_label "
    f"FROM \"{_RECODE}\" WHERE var = 'edu')"
)
_UNPIVOT_ON = ", ".join(_SCENARIO_COLS)


def _indicator_sql(dep: str, value_name: str, *, has_edu: bool) -> str:
    """Unpivot a wide indicator file to (..., scenario, <value_name>), decoding
    region (and education, when present) via the recode dictionary."""
    ctes = [_REG_CTE]
    edu_select = ""
    edu_join = ""
    if has_edu:
        ctes.append(_EDU_CTE)
        edu_select = "l.edu, e.edu_label,"
        edu_join = "LEFT JOIN edu e ON l.edu = e.edu"
    ctes.append(
        f"long AS (UNPIVOT \"{dep}\" ON {_UNPIVOT_ON} "
        f"INTO NAME scenario VALUE value)"
    )
    return f"""
        WITH {', '.join(ctes)}
        SELECT
            l.region,
            r.region_name,
            CAST(l.Time AS INTEGER) AS year,
            l.sex,
            {edu_select}
            CAST(l.agest AS INTEGER) AS age_start,
            l.scenario,
            CAST(l.value AS DOUBLE) AS {value_name}
        FROM long l
        LEFT JOIN reg r ON l.region = r.region
        {edu_join}
        WHERE l.value IS NOT NULL
    """


# SRB has no sex/edu/agest dimensions — handled inline.
_SRB_SQL = f"""
    WITH {_REG_CTE},
    long AS (UNPIVOT "wittgenstein-centre-sex-ratio-at-birth" ON {_UNPIVOT_ON}
             INTO NAME scenario VALUE value)
    SELECT
        l.region,
        r.region_name,
        CAST(l.Time AS INTEGER) AS year,
        l.scenario,
        CAST(l.value AS DOUBLE) AS sex_ratio_at_birth
    FROM long l
    LEFT JOIN reg r ON l.region = r.region
    WHERE l.value IS NOT NULL
"""

_PROJ_SQL = f"""
    WITH {_REG_CTE}, {_EDU_CTE}
    SELECT
        p.region,
        r.region_name,
        CAST(p.Time AS INTEGER) AS year,
        p.sex,
        p.edu,
        e.edu_label,
        CAST(p.agest AS INTEGER) AS age_start,
        p.scenario,
        CAST(p.pop AS DOUBLE) AS population,
        CAST(p.births AS DOUBLE) AS births,
        CAST(p.emi AS DOUBLE) AS emigrants,
        CAST(p.imm AS DOUBLE) AS immigrants,
        CAST(p.deaths AS DOUBLE) AS deaths
    FROM "wittgenstein-centre-projection-results" p
    LEFT JOIN reg r ON p.region = r.region
    LEFT JOIN edu e ON p.edu = e.edu
"""

_RECODE_SQL = f"""
    SELECT
        var AS variable,
        varnm AS variable_label,
        varval AS code,
        varvaldesc AS description
    FROM "{_RECODE}"
    WHERE var IS NOT NULL
"""

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="wittgenstein-centre-asfr-transform",
        deps=["wittgenstein-centre-asfr", _RECODE],
        sql=_indicator_sql("wittgenstein-centre-asfr", "asfr_births_per_1000_women", has_edu=True),
    ),
    SqlNodeSpec(
        id="wittgenstein-centre-edu-proportions-transform",
        deps=["wittgenstein-centre-edu-proportions", _RECODE],
        sql=_indicator_sql("wittgenstein-centre-edu-proportions", "proportion", has_edu=True),
    ),
    SqlNodeSpec(
        id="wittgenstein-centre-mean-years-schooling-transform",
        deps=["wittgenstein-centre-mean-years-schooling", _RECODE],
        sql=_indicator_sql("wittgenstein-centre-mean-years-schooling", "mean_years_schooling", has_edu=False),
    ),
    SqlNodeSpec(
        id="wittgenstein-centre-survival-ratios-transform",
        deps=["wittgenstein-centre-survival-ratios", _RECODE],
        sql=_indicator_sql("wittgenstein-centre-survival-ratios", "survival_ratio", has_edu=True),
    ),
    SqlNodeSpec(
        id="wittgenstein-centre-sex-ratio-at-birth-transform",
        deps=["wittgenstein-centre-sex-ratio-at-birth", _RECODE],
        sql=_SRB_SQL,
    ),
    SqlNodeSpec(
        id="wittgenstein-centre-projection-results-transform",
        deps=["wittgenstein-centre-projection-results", _RECODE],
        sql=_PROJ_SQL,
    ),
    SqlNodeSpec(
        id="wittgenstein-centre-recode-dictionary-transform",
        deps=[_RECODE],
        sql=_RECODE_SQL,
    ),
]
