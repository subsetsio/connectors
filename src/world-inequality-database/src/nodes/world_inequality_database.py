"""World Inequality Database (WID.world) connector.

Single subset: `values` — the long-format observation corpus of the entire
database. Access is the official bulk export, one persistent ZIP holding the
whole database (https://wid.world/bulk_download/wid_all_data.zip, ~850MB),
containing one `WID_data_XX.csv` per area (423 areas) with a uniform schema:
country;variable;percentile;year;value;age;pop (semicolon-separated).

Fetch shape: stateless full re-pull. The bulk export has no incremental/delta
filter — it is a single full snapshot refreshed roughly annually (~July), so we
re-download and overwrite the whole corpus each run. Revisions and the shifting
reference year are picked up for free. The download streams to a temp file and
the ZIP members are parsed in bounded-memory batches into one streamed parquet,
so the ~850MB payload never lands in RAM whole.
"""

import os
import tempfile
import zipfile

import pyarrow as pa
import pyarrow.csv as pacsv
import pyarrow.parquet as pq  # noqa: F401  (ParquetWriter used via raw_parquet_writer)

from subsets_utils import (
    NodeSpec,
    SqlNodeSpec,
    get_client,
    raw_parquet_writer,
    transient_retry,
)

BULK_URL = "https://wid.world/bulk_download/wid_all_data.zip"

# Uniform schema of every WID_data_XX.csv member.
EXPECTED_HEADER = ["country", "variable", "percentile", "year", "value", "age", "pop"]

SCHEMA = pa.schema([
    ("country", pa.string()),
    ("variable", pa.string()),
    ("percentile", pa.string()),
    ("year", pa.int32()),
    ("value", pa.float64()),
    ("age", pa.string()),
    ("pop", pa.string()),
])

# pyarrow CSV options: force the WID schema (so type inference can't drift
# member-to-member), treat empty / "NA" as null in the numeric columns only,
# and skip the occasional malformed row instead of aborting the whole pull.
# Parsing in pyarrow's C++ reader is ~an order of magnitude faster than a
# Python csv.reader row loop over the corpus's tens of millions of rows.
def _skip_invalid_row(_row) -> str:
    return "skip"


_READ_OPTS = pacsv.ReadOptions(block_size=1 << 24)
_PARSE_OPTS = pacsv.ParseOptions(delimiter=";", invalid_row_handler=_skip_invalid_row)
_CONVERT_OPTS = pacsv.ConvertOptions(
    column_types={
        "country": pa.string(),
        "variable": pa.string(),
        "percentile": pa.string(),
        "year": pa.int32(),
        "value": pa.float64(),
        "age": pa.string(),
        "pop": pa.string(),
    },
    null_values=["", "NA"],
    strings_can_be_null=False,
)


@transient_retry()
def _download_bulk_zip(dest_path: str) -> None:
    """Stream the full WID bulk ZIP to a local temp file (bounded memory)."""
    client = get_client()
    with client.stream("GET", BULK_URL, timeout=(30.0, 300.0)) as resp:
        resp.raise_for_status()
        with open(dest_path, "wb") as f:
            for chunk in resp.iter_bytes(1 << 20):
                f.write(chunk)


def _parse_member(zf: zipfile.ZipFile, member: str, writer) -> None:
    """Parse one WID_data_XX.csv member into the streamed raw parquet.

    The member is read into a buffer (each is a small slice of the ~850MB
    corpus) and parsed by pyarrow's streaming CSV reader, so peak memory is one
    member plus one record batch. The header is validated against the uniform
    WID layout; a format change fails loudly rather than writing garbage.
    """
    reader = pacsv.open_csv(
        pa.BufferReader(zf.read(member)),
        read_options=_READ_OPTS,
        parse_options=_PARSE_OPTS,
        convert_options=_CONVERT_OPTS,
    )
    assert reader.schema.names == EXPECTED_HEADER, (
        f"{member}: unexpected header {reader.schema.names!r}, "
        f"expected {EXPECTED_HEADER!r}"
    )
    for batch in reader:
        if batch.num_rows:
            # cast is a positional no-op here (types are forced above) — it just
            # guarantees the writer always sees the exact SCHEMA.
            writer.write_table(pa.Table.from_batches([batch]).cast(SCHEMA))


def fetch_values(node_id: str) -> None:
    asset = node_id  # the runtime passes the spec id; it IS the asset name

    tmp = tempfile.NamedTemporaryFile(suffix=".zip", delete=False)
    tmp.close()
    try:
        _download_bulk_zip(tmp.name)

        with zipfile.ZipFile(tmp.name) as zf:
            members = sorted(
                n for n in zf.namelist()
                if os.path.basename(n).startswith("WID_data_") and n.endswith(".csv")
            )
            assert members, "no WID_data_*.csv members found in bulk ZIP — format changed"

            with raw_parquet_writer(asset, SCHEMA) as writer:
                for member in members:
                    _parse_member(zf, member, writer)
    finally:
        os.unlink(tmp.name)


ENTITY_IDS = ["values"]

DOWNLOAD_SPECS = [
    NodeSpec(
        id=f"world-inequality-database-{eid.lower().replace('_', '-')}",
        fn=fetch_values,
        kind="download",
    )
    for eid in ENTITY_IDS
]

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id=f"{s.id}-transform",
        deps=[s.id],
        sql=f'''
            SELECT
                country,
                variable,
                percentile,
                CAST(year AS INTEGER)  AS year,
                CAST(value AS DOUBLE)  AS value,
                age,
                pop
            FROM "{s.id}"
            WHERE value IS NOT NULL
        ''',
    )
    for s in DOWNLOAD_SPECS
]
