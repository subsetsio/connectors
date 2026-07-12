"""OpenPowerlifting connector — the full powerlifting meet-results corpus.

Single entity (`results`): OpenPowerlifting publishes its entire database nightly
as one zipped, fully-denormalized CSV (one row per lifter-per-meet, ~3.96M rows)
at a stable URL, no auth, no incremental-query parameter. The whole corpus is
~166MB zipped, so the correct shape is a **stateless full re-pull**: re-fetch the
zip every run and overwrite — revisions and late corrections are picked up for
free because no watermark is trusted.

Raw is streamed CSV -> parquet with every column kept as a string. The CSV mixes
numeric values with sentinels ('DQ'/'NS'/'G' in Place, '+' in WeightClassKg,
negative weights for failed attempts, 'n.5' approximate ages), so typing is left
entirely to the transform, which TRY_CASTs the columns it publishes.
"""
import csv
import io
import zipfile

import pyarrow as pa
import pyarrow.csv as pacsv
from subsets_utils import (
    NodeSpec,
    get,
    raw_parquet_writer,
)

RESULTS_URL = "https://openpowerlifting.gitlab.io/opl-csv/files/openpowerlifting-latest.zip"


def _download(url: str) -> bytes:
    resp = get(url, timeout=(10.0, 600.0))
    resp.raise_for_status()
    return resp.content


def fetch_results(node_id: str) -> None:
    asset = node_id  # the runtime passes the spec id; it IS the asset name

    zf = zipfile.ZipFile(io.BytesIO(_download(RESULTS_URL)))
    csv_members = [n for n in zf.namelist() if n.lower().endswith(".csv")]
    if len(csv_members) != 1:
        raise AssertionError(
            f"expected exactly 1 CSV inside the zip, found {csv_members}"
        )
    member = csv_members[0]

    # Read the header to pin an all-string schema; keep every published column as
    # VARCHAR and let the transform cast. Robust to the CSV's mixed sentinels.
    with zf.open(member) as fh:
        header = next(csv.reader(io.TextIOWrapper(fh, encoding="utf-8")))
    schema = pa.schema([(c, pa.string()) for c in header])

    read_opts = pacsv.ReadOptions(block_size=64 << 20)
    convert_opts = pacsv.ConvertOptions(
        column_types={c: pa.string() for c in header}
    )
    with zf.open(member) as fh:
        reader = pacsv.open_csv(
            fh, read_options=read_opts, convert_options=convert_opts
        )
        with raw_parquet_writer(asset, schema) as writer:
            for batch in reader:
                writer.write_table(pa.Table.from_batches([batch], schema=schema))


DOWNLOAD_SPECS = [
    NodeSpec(id="openpowerlifting-results", fn=fetch_results, kind="download"),
]
