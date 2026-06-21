"""Economic Policy Institute — State of Working America (SWA) Data Library.

Mechanism (chosen): `bulk_csv_zip`. EPI publishes the whole SWA Data Library as a
single GitHub release asset (`epi_swa_data_library.zip`, ~220 MB) holding one CSV
per indicator. Every CSV shares one flat long schema:

    data_version, indicator, measure, date_interval, year, quarter, month,
    geo_type, geo_name, geo_code, group, group_value, value

There is no per-indicator download URL and no incremental query — the ZIP is the
only bulk path, re-pulled in full each refresh (shape 1, stateless full re-pull).
Each indicator is one publishable subset, so each download spec downloads the ZIP
and extracts its own indicator's CSV (matched by the `indicator` display name,
with the known filename as the fast path), streaming it to a raw parquet asset.
The big labor-force CSVs reach ~260 MB uncompressed, so extraction streams batch
by batch rather than materialising the whole table.

Raw is written verbatim as all-string columns (the source mixes 'NA' sentinels
and empty strings across numeric fields); the SQL transform does the typing.
"""

import io
import zipfile

import pyarrow as pa
import pyarrow.csv as pacsv

from subsets_utils import (
    NodeSpec,
    SqlNodeSpec,
    get,
    transient_retry,
    raw_parquet_writer,
)
from constants import ENTITY_IDS, INDICATOR_NAMES, CSV_FILENAMES

SLUG = "economic-policy-institute"
ZIP_URL = "https://github.com/Economic/data/releases/latest/download/epi_swa_data_library.zip"

# The shared long schema of every SWA CSV. Read everything as string and let the
# transform cast — the source uses 'NA'/'' sentinels across the numeric fields.
COLUMNS = [
    "data_version", "indicator", "measure", "date_interval", "year", "quarter",
    "month", "geo_type", "geo_name", "geo_code", "group", "group_value", "value",
]
RAW_SCHEMA = pa.schema([(c, pa.string()) for c in COLUMNS])


def _entity_id_from_node(node_id: str) -> str:
    """Recover the original entity id from a spec id, matching the
    f"{SLUG}-{eid.lower().replace('_','-')}" rule used to build the specs."""
    suffix = node_id[len(SLUG) + 1:]                  # strip "economic-policy-institute-"
    for eid in ENTITY_IDS:
        if eid.lower().replace("_", "-") == suffix:
            return eid
    raise KeyError(f"no entity id maps to node {node_id!r}")


@transient_retry()  # 6 attempts, exponential backoff over transient/429/5xx
def _download_zip_bytes() -> bytes:
    resp = get(ZIP_URL, timeout=(10.0, 300.0))
    resp.raise_for_status()
    return resp.content


def _member_for(zf: zipfile.ZipFile, entity_id: str) -> str:
    """Locate the ZIP member for this indicator. Fast path is the known filename;
    fall back to matching the `indicator` display-name column so a renamed file
    still resolves. Raises loudly if neither resolves — a silent wrong-file pick
    would publish the wrong indicator."""
    names = set(zf.namelist())
    expected_name = INDICATOR_NAMES[entity_id]

    fast = CSV_FILENAMES.get(entity_id)
    if fast and fast in names:
        if _member_indicator(zf, fast) == expected_name:
            return fast

    # filename drifted — scan members for the one whose `indicator` matches
    for member in names:
        if member.endswith(".csv") and _member_indicator(zf, member) == expected_name:
            return member
    raise KeyError(
        f"{entity_id}: no ZIP member found for indicator {expected_name!r} "
        f"(tried filename {fast!r}); ZIP members: {sorted(names)}"
    )


def _member_indicator(zf: zipfile.ZipFile, member: str) -> str | None:
    """Read the `indicator` value from the first data row of a CSV member."""
    with zf.open(member) as fh:
        text = io.TextIOWrapper(fh, encoding="utf-8")
        header = text.readline().rstrip("\n").split(",")
        if "indicator" not in header:
            return None
        idx = header.index("indicator")
        first = text.readline().rstrip("\n")
        if not first:
            return None
        # values here are simple tokens (no embedded commas in the indicator name)
        return first.split(",")[idx]


def fetch_one(node_id: str) -> None:
    asset = node_id  # the spec id IS the raw asset name
    entity_id = _entity_id_from_node(node_id)

    zf = zipfile.ZipFile(io.BytesIO(_download_zip_bytes()))
    member = _member_for(zf, entity_id)

    read_opts = pacsv.ReadOptions(block_size=16 << 20)
    parse_opts = pacsv.ParseOptions(newlines_in_values=True)
    # keep raw verbatim: force every column to string, null nothing
    convert_opts = pacsv.ConvertOptions(
        column_types={c: pa.string() for c in COLUMNS},
        null_values=[],
        strings_can_be_null=False,
    )

    with zf.open(member) as fh:
        reader = pacsv.open_csv(fh, read_opts, parse_opts, convert_opts)
        with raw_parquet_writer(asset, RAW_SCHEMA) as writer:
            for batch in reader:
                if batch.num_rows:
                    writer.write_batch(batch.select(COLUMNS))


DOWNLOAD_SPECS = [
    NodeSpec(
        id=f"{SLUG}-{eid.lower().replace('_', '-')}",
        fn=fetch_one,
        kind="download",
    )
    for eid in ENTITY_IDS
]


# ---- transforms: one published long-format table per indicator ---------------
# Build a typed DATE from the (date_interval, year, quarter, month) columns,
# rename the reserved `group` column, and cast value to DOUBLE (dropping the
# 'NA'/'' sentinels). Same shape for every indicator; the dep view differs.
def _transform_sql(dep_id: str) -> str:
    return f'''
        SELECT
            CASE date_interval
                WHEN 'year'    THEN make_date(TRY_CAST(year AS INTEGER), 1, 1)
                WHEN 'quarter' THEN make_date(TRY_CAST(year AS INTEGER),
                                              (TRY_CAST(quarter AS INTEGER) - 1) * 3 + 1, 1)
                WHEN 'month'   THEN make_date(TRY_CAST(year AS INTEGER),
                                              TRY_CAST(month AS INTEGER), 1)
            END                                   AS date,
            date_interval                         AS frequency,
            indicator,
            measure,
            geo_type,
            geo_name,
            geo_code,
            NULLIF("group", '')                   AS group_name,
            group_value,
            TRY_CAST(value AS DOUBLE)             AS value
        FROM "{dep_id}"
        WHERE TRY_CAST(value AS DOUBLE) IS NOT NULL
          AND TRY_CAST(year AS INTEGER) IS NOT NULL
    '''


TRANSFORM_SPECS = [
    SqlNodeSpec(
        id=f"{s.id}-transform",
        deps=[s.id],
        sql=_transform_sql(s.id),
    )
    for s in DOWNLOAD_SPECS
]
