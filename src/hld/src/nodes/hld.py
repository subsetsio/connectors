"""HLD — Human Life-Table Database (lifetable.de).

One subset: the full life-table corpus. The whole database ships as a single
ZIP (`hld.zip`, ~56MB) containing one member named `res` — a ~214MB CSV with
~2.3M rows (one row per country/year/life-table-type/sex/age group) across 142
countries/areas. We re-pull the whole ZIP every run (stateless full re-pull):
the source overwrites it in place a few times a year, so there is no incremental
filter and a full snapshot is cheap enough.

Data-quality note: a small fraction of rows (~1.5k of 2.3M, certain ethnicity
subpopulations for GBR/ISL/ITA/MYS/NZL) are written with a comma decimal
separator, producing 25-26 fields instead of 21. Those rows are unparseable as
CSV and are skipped (logged) rather than guessed at; everything else parses
cleanly. Missing numeric cells use '.' as the null marker.
"""

import io
import logging
import zipfile

import pyarrow as pa
import pyarrow.csv as pacsv

from subsets_utils import NodeSpec, SqlNodeSpec, get, transient_retry, save_raw_parquet

logger = logging.getLogger(__name__)

BULK_URL = "https://www.lifetable.de/File/GetDocument/data/hld.zip"
ZIP_MEMBER = "res"

# Column order in the upstream CSV (header is present but we name explicitly so
# the contract is pinned in code). The four measure-of-mortality code columns
# (region/residence/ethnicity/socdem) are categorical codes kept as strings;
# the life-table quantities are read as doubles (some abridged tables carry
# fractional person-years), the dimensions as ints.
COLUMN_NAMES = [
    "country", "region", "residence", "ethnicity", "socdem", "version", "ref_id",
    "year1", "year2", "type_lt", "sex", "age", "age_int",
    "mx", "qx", "lx", "dx", "Lx", "Tx", "ex", "ex_orig",
]
_STRING_COLS = ["country", "region", "residence", "ethnicity", "socdem", "version", "ref_id"]
_INT_COLS = ["year1", "year2", "type_lt", "sex", "age", "age_int"]
_FLOAT_COLS = ["mx", "qx", "lx", "dx", "Lx", "Tx", "ex", "ex_orig"]

COLUMN_TYPES = {c: pa.string() for c in _STRING_COLS}
COLUMN_TYPES.update({c: pa.int64() for c in _INT_COLS})
COLUMN_TYPES.update({c: pa.float64() for c in _FLOAT_COLS})


@transient_retry()  # 6 attempts, exponential backoff; retries 429/5xx/network
def _fetch_bulk_zip() -> bytes:
    resp = get(BULK_URL, timeout=(10.0, 300.0))
    resp.raise_for_status()
    return resp.content


def fetch_life_tables(node_id: str) -> None:
    asset = node_id  # the runtime passes the spec id; it IS the asset name

    content = _fetch_bulk_zip()
    with zipfile.ZipFile(io.BytesIO(content)) as zf:
        raw = zf.read(ZIP_MEMBER)
    del content

    skipped = 0

    def _on_invalid_row(row) -> str:
        nonlocal skipped
        skipped += 1
        return "skip"

    table = pacsv.read_csv(
        io.BytesIO(raw),
        read_options=pacsv.ReadOptions(column_names=COLUMN_NAMES, skip_rows=1),
        parse_options=pacsv.ParseOptions(invalid_row_handler=_on_invalid_row),
        convert_options=pacsv.ConvertOptions(
            column_types=COLUMN_TYPES,
            null_values=["", ".", "NA", "na"],
            strings_can_be_null=True,
            quoted_strings_can_be_null=True,
        ),
    )
    del raw

    logger.info(
        "hld: parsed %d life-table rows (%d malformed comma-decimal rows skipped)",
        table.num_rows,
        skipped,
    )
    if table.num_rows == 0:
        raise AssertionError("hld bulk parse produced 0 rows — upstream format change?")

    save_raw_parquet(table, asset)


DOWNLOAD_SPECS = [
    NodeSpec(id="hld-life-tables", fn=fetch_life_tables, kind="download"),
]


TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="hld-life-tables-transform",
        deps=["hld-life-tables"],
        sql='''
            SELECT
                country,
                NULLIF(region, '0')    AS region,
                NULLIF(residence, '0') AS residence,
                NULLIF(ethnicity, '0') AS ethnicity,
                NULLIF(socdem, '0')    AS socdem,
                CAST(version AS INTEGER) AS version,
                ref_id,
                CAST(year1 AS INTEGER) AS year_start,
                CAST(year2 AS INTEGER) AS year_end,
                CAST(type_lt AS INTEGER) AS life_table_type,
                CAST(sex AS INTEGER)     AS sex,
                CAST(age AS INTEGER)     AS age,
                CAST(age_int AS INTEGER) AS age_interval,
                CAST(mx AS DOUBLE)  AS death_rate_mx,
                CAST(qx AS DOUBLE)  AS death_probability_qx,
                CAST(lx AS DOUBLE)  AS survivors_lx,
                CAST(dx AS DOUBLE)  AS deaths_dx,
                CAST("Lx" AS DOUBLE) AS person_years_Lx,
                CAST("Tx" AS DOUBLE) AS total_years_Tx,
                CAST(ex AS DOUBLE)      AS life_expectancy_ex,
                CAST(ex_orig AS DOUBLE) AS life_expectancy_orig_ex
            FROM "hld-life-tables"
            WHERE country IS NOT NULL
        ''',
    ),
]
