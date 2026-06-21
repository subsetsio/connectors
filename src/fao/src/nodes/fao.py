"""FAO / FAOSTAT connector.

Mechanism: bulk_csv (research-chosen). FAOSTAT publishes one stable ZIP per
statistical domain at https://bulks-faostat.fao.org/production/. The manifest
``datasets_E.json`` lists every domain with its canonical
``{Name}_E_All_Data_(Normalized).zip`` FileLocation. Each ZIP bundles a main
long/tidy "Normalized" CSV (the data) plus small codelist CSVs (areas, items,
elements, flags) which we ignore.

Fetch shape: **stateless full re-pull** (shape 1). Each domain is a single
self-contained ZIP re-fetched in full every refresh and overwritten — FAOSTAT
exposes no row-level changed-since filter, and re-pulling picks up revisions and
late corrections for free. The largest domain (Detailed trade matrix, TM) is
~52M rows / ~410MB zip, so the CSV is streamed out of the ZIP straight into a
row-group-streamed parquet to keep memory bounded; we never materialise the full
table in RAM.

Raw format: parquet with **all columns typed as string**. The Normalized schema
varies across domains (item- vs indicator- vs survey-keyed, trade matrices carry
reporter/partner, monthly domains carry Months) — forcing strings makes the
generic loader deterministic across all 62 domains and defers numeric typing to
the transform. Column names are sanitised to snake_case so the published Delta
table avoids the spaces/parentheses Delta forbids in column names.
"""

import io
import os
import tempfile
import zipfile

import pyarrow as pa
import pyarrow.csv as pacsv
import pyarrow.parquet as pq

from subsets_utils import (
    NodeSpec,
    SqlNodeSpec,
    get,
    raw_parquet_writer,
    transient_retry,
)

MANIFEST_URL = "https://bulks-faostat.fao.org/production/datasets_E.json"
ID_PREFIX = "fao-"

# The entity union (rank-active FAOSTAT domain codes) — inlined per the catalog
# connector pattern; module-level file I/O is not allowed.
from constants import ENTITY_IDS


@transient_retry()
def _load_manifest() -> list:
    resp = get(MANIFEST_URL, timeout=(10.0, 60.0))
    resp.raise_for_status()
    return resp.json()["Datasets"]["Dataset"]


@transient_retry()
def _download_zip(url: str) -> bytes:
    resp = get(url, timeout=(10.0, 600.0))
    resp.raise_for_status()
    return resp.content


def _sanitize(name: str) -> str:
    """FAOSTAT header -> snake_case column name safe for Delta (no spaces/parens)."""
    s = name.strip().lower()
    for ch in "()[]{}/\\,;=\t\n":
        s = s.replace(ch, " ")
    s = s.replace("-", " ")
    return "_".join(s.split()) or "col"


def _dedupe(names: list) -> list:
    seen, out = {}, []
    for n in names:
        if n in seen:
            seen[n] += 1
            out.append(f"{n}_{seen[n]}")
        else:
            seen[n] = 0
            out.append(n)
    return out


def _read_header_names(member_stream) -> list:
    """Read just the first (header) line. FAOSTAT headers are pure-ASCII,
    unquoted, and contain no embedded commas, so a plain split is safe
    regardless of the body's encoding."""
    buf = b""
    while b"\n" not in buf:
        chunk = member_stream.read(8192)
        if not chunk:
            break
        buf += chunk
    line = buf.split(b"\n", 1)[0].decode("latin-1").rstrip("\r")
    return line.split(",")


class _Cp1252ToUtf8(io.RawIOBase):
    """Streaming byte transcoder: read CP1252/Latin-1 bytes, emit UTF-8.

    Older FAOSTAT domains (e.g. CBH, FBSH, FT) are CP1252-encoded ('Côte
    d'Ivoire' carries a 0xf4 byte) which pyarrow's UTF-8 CSV reader rejects.
    CP1252 is single-byte, so each chunk transcodes independently with no
    risk of splitting a multibyte sequence across reads. errors='replace'
    guarantees the second pass never fails on an undefined code point.

    Subclasses io.RawIOBase so pyarrow gets the full read/readable/closed
    file protocol it expects from a Python input stream.
    """

    def __init__(self, raw):
        super().__init__()
        self._raw = raw
        self._buf = b""

    def readable(self):
        return True

    def readinto(self, b):
        n = len(b)
        while len(self._buf) < n:
            chunk = self._raw.read(65536)
            if not chunk:
                break
            self._buf += chunk.decode("cp1252", "replace").encode("utf-8")
        take = self._buf[:n]
        b[: len(take)] = take
        self._buf = self._buf[len(take):]
        return len(take)


def _csv_member_to_parquet(zip_path: str, member: str, asset: str, *, transcode: bool) -> None:
    with zipfile.ZipFile(zip_path) as zf:
        with zf.open(member) as f:
            orig_names = _read_header_names(f)
        safe_names = _dedupe([_sanitize(n) for n in orig_names])
        out_schema = pa.schema([(n, pa.string()) for n in safe_names])

        convert = pacsv.ConvertOptions(
            column_types={n: pa.string() for n in orig_names},
            strings_can_be_null=True,
            null_values=[""],
        )
        read_opts = pacsv.ReadOptions(block_size=64 << 20)

        with zf.open(member) as f:
            src = _Cp1252ToUtf8(f) if transcode else f
            reader = pacsv.open_csv(src, read_options=read_opts, convert_options=convert)
            with raw_parquet_writer(asset, out_schema) as writer:
                for batch in reader:
                    writer.write_batch(
                        pa.RecordBatch.from_arrays(batch.columns, names=safe_names)
                    )


def fetch_one(node_id: str) -> None:
    asset = node_id  # the runtime passes the spec id; it IS the asset name
    code = node_id[len(ID_PREFIX):].upper()

    rec = next((d for d in _load_manifest() if d.get("DatasetCode") == code), None)
    if rec is None:
        raise RuntimeError(f"{code}: domain not present in FAOSTAT manifest {MANIFEST_URL}")
    url = rec["FileLocation"]

    content = _download_zip(url)
    tmp = tempfile.NamedTemporaryFile(suffix=".zip", delete=False)
    try:
        tmp.write(content)
        tmp.close()
        del content
        with zipfile.ZipFile(tmp.name) as zf:
            members = zf.namelist()
            main = [m for m in members if m.lower().endswith("(normalized).csv")]
            if not main:
                raise RuntimeError(f"{code}: no '(Normalized).csv' member in {members}")
            member = main[0]

        # Most domains are UTF-8; older ones (CBH, FBSH, FT, ...) are CP1252.
        # Try UTF-8 first (no overhead, incl. the huge TM domain); on a UTF-8
        # conversion error re-parse the same local ZIP through the transcoder.
        # raw_parquet_writer truncates the output, so the retry starts clean.
        try:
            _csv_member_to_parquet(tmp.name, member, asset, transcode=False)
        except pa.ArrowInvalid as e:
            if "utf8" not in str(e).lower() and "utf-8" not in str(e).lower():
                raise
            _csv_member_to_parquet(tmp.name, member, asset, transcode=True)
    finally:
        os.unlink(tmp.name)


DOWNLOAD_SPECS = [
    NodeSpec(
        id=f"{ID_PREFIX}{eid.lower().replace('_', '-')}",
        fn=fetch_one,
        kind="download",
    )
    for eid in ENTITY_IDS
]


# One published Delta table per domain. Universal across every Normalized domain:
# a numeric `value` measure plus `element`/`flag`/`unit` dimensions. The transform
# is a thin typed pass — keep every (string) dimension column, retype `value` to
# DOUBLE, and drop rows whose value is empty/non-numeric (so an all-flag, no-data
# row never publishes a null measure).
TRANSFORM_SPECS = [
    SqlNodeSpec(
        id=f"{s.id}-transform",
        deps=[s.id],
        sql=f'''
            SELECT * REPLACE (TRY_CAST("value" AS DOUBLE) AS "value")
            FROM "{s.id}"
            WHERE TRY_CAST("value" AS DOUBLE) IS NOT NULL
        ''',
    )
    for s in DOWNLOAD_SPECS
]
