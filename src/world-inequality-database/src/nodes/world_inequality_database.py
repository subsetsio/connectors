"""World Inequality Database (WID.world) connector.

Three subsets, all carved out of ONE artifact: the official bulk export at
https://wid.world/bulk_download/wid_all_data.zip (~883MB), a persistent ZIP
holding the entire database. Its 848 members are `WID_countries.csv`,
`README.md`, and a `WID_data_XX.csv` + `WID_metadata_XX.csv` pair for each of
423 areas. Every CSV is semicolon-separated.

  values     the long-format observation corpus (all 423 `WID_data_*.csv`)
  variables  per-area/variable metadata (all 423 `WID_metadata_*.csv`)
  countries  the area-code dictionary (`WID_countries.csv`)

Download nodes are independent, so they cannot share one fetch. Rather than
pull 883MB three times, only `values` streams the whole ZIP (it needs ~all of
it: the data members are 859MB of the 883MB). `variables` and `countries` read
just their own members over HTTP range requests against the ZIP's central
directory — 24MB and 4KB respectively. The server advertises `Accept-Ranges:
bytes`; if that ever stops holding, those two nodes fail loudly rather than
silently degrading.

Fetch shape: stateless full re-pull. The export exposes no incremental/delta
filter — it is one full snapshot refreshed roughly annually (~July), so each
run re-reads and overwrites. Revisions and the shifting reference year come
along for free. MAINTAIN_SPECS gates whether a run refetches at all, off the
ZIP's ETag/Last-Modified and `PARSE_REVISION`.

Schema drift, measured and normalized here rather than left to the transform:
the aggregate-region members (QE, WO, ...) omit `data_quality` from the data
CSVs and `data_quality_score` from the metadata CSVs, and `data_quality` is
integral in some members and fractional in others (FR carries 0.0144). Both
columns are therefore pinned to float64 and back-filled as null where absent,
so every member conforms to one declared schema.

Two upstream quirks worth knowing before touching the parse:

  * Namibia's area code is the literal string `NA`, which every CSV reader on
    earth wants to read as a null. See `_convert_opts`.
  * 12 of the 423 areas ship header-only members (47 bytes) in BOTH the data
    and metadata sets — `Al`, `ON`, `SW`, `XC`, `XE`, `XK`, `XQ` and the
    `ON/OO/OP/OQ/XQ`-`MER` variants. They are placeholders upstream, so only
    411 areas ever appear in the raw. The coverage waivers on the two
    per-area specs record exactly that gap.
"""

import io
import os
import tempfile
import zipfile

import pyarrow as pa
import pyarrow.csv as pacsv

from subsets_utils import (
    MaintainSpec,
    NodeSpec,
    get,
    get_client,
    load_state,
    raw_asset_exists,
    raw_parquet_writer,
    record_source_signature,
    save_raw_parquet,
    save_state,
    source_unchanged,
    transient_retry,
)

BULK_URL = "https://wid.world/bulk_download/wid_all_data.zip"

# Bump whenever a change here invalidates raw produced by the previous code.
#
# The maintain check asks "has the SOURCE changed since we last fetched?" — it
# compares the ZIP's ETag against the signature recorded at the last successful
# fetch. It cannot see that OUR parse changed, so on a stateless full-snapshot
# source like this one a fetch bug is self-preserving: the ETag still matches,
# every run skips the fetch, and the bad raw is never rewritten. Stamping the
# revision into the asset state and requiring it to match closes that loop.
#
#   1  initial
#   2  null_values no longer swallows Namibia's `NA` area code
PARSE_REVISION = 2
_REVISION_KEY = "parse_revision"

# A sanity floor on the area count, not the true universe: WID ships 423 areas
# today. A ZIP that suddenly holds a handful of members means the export broke
# or moved, and we must fail rather than publish a truncated corpus.
MIN_AREA_MEMBERS = 300

DATA_COLUMNS = ["country", "variable", "percentile", "year", "value", "age", "pop", "data_quality"]
DATA_SCHEMA = pa.schema([
    ("country", pa.string()),
    ("variable", pa.string()),
    ("percentile", pa.string()),
    ("year", pa.int32()),
    ("value", pa.float64()),
    ("age", pa.int32()),
    ("pop", pa.string()),
    ("data_quality", pa.float64()),
])

METADATA_COLUMNS = [
    "country", "variable", "age", "pop", "countryname", "shortname", "simpledes",
    "technicaldes", "shorttype", "longtype", "shortpop", "longpop", "shortage",
    "longage", "unit", "source", "method", "extrapolation", "data_points",
    "data_quality_score",
]
METADATA_SCHEMA = pa.schema(
    [(c, pa.int32() if c == "age" else pa.float64() if c == "data_quality_score" else pa.string())
     for c in METADATA_COLUMNS]
)

COUNTRY_COLUMNS = ["alpha2", "titlename", "shortname", "region", "region2"]
COUNTRY_SCHEMA = pa.schema([(c, pa.string()) for c in COUNTRY_COLUMNS])

_PARSE_OPTS = pacsv.ParseOptions(delimiter=";")
_READ_OPTS = pacsv.ReadOptions(block_size=1 << 24)


def _convert_opts(schema: pa.Schema) -> pacsv.ConvertOptions:
    """Force the declared schema onto a member.

    `include_columns` pins the output column order; `include_missing_columns`
    null-fills the quality columns the aggregate-region members omit. Together
    they make per-member type inference impossible, which is the point — the
    schema is the contract, and a member that cannot be coerced into it raises.

    `null_values` must stay exactly `[""]`. It overrides pyarrow's default
    token list, which includes "NA" — and "NA" is Namibia's area code, the sole
    place that token occurs anywhere in the export. Adding it back nulls the
    `country` column of all 1.15M Namibian rows.
    """
    return pacsv.ConvertOptions(
        column_types={f.name: f.type for f in schema},
        include_columns=list(schema.names),
        include_missing_columns=True,
        null_values=[""],
        strings_can_be_null=True,
    )


class _RangeReader(io.RawIOBase):
    """A seekable read-only file over an HTTP resource, backed by range GETs.

    Lets `zipfile` parse the central directory and inflate individual members
    of the 883MB export without downloading it. Every request goes through
    `subsets_utils.get`, so transient failures are already retried.
    """

    def __init__(self, url: str):
        self.url = url
        self.pos = 0
        resp = get_client().head(url, timeout=(10.0, 60.0))
        resp.raise_for_status()
        if resp.headers.get("Accept-Ranges") != "bytes":
            raise RuntimeError(
                f"{url} no longer advertises 'Accept-Ranges: bytes' — the ranged "
                "member reads this node depends on are unavailable"
            )
        self.size = int(resp.headers["Content-Length"])

    def readable(self) -> bool:
        return True

    def seekable(self) -> bool:
        return True

    def tell(self) -> int:
        return self.pos

    def seek(self, offset: int, whence: int = os.SEEK_SET) -> int:
        if whence == os.SEEK_SET:
            self.pos = offset
        elif whence == os.SEEK_CUR:
            self.pos += offset
        else:
            self.pos = self.size + offset
        return self.pos

    def read(self, size: int = -1) -> bytes:
        if size is None or size < 0:
            size = self.size - self.pos
        if size == 0 or self.pos >= self.size:
            return b""
        last = min(self.pos + size, self.size) - 1
        resp = get(self.url, headers={"Range": f"bytes={self.pos}-{last}"}, timeout=(10.0, 120.0))
        resp.raise_for_status()
        chunk = resp.content
        self.pos += len(chunk)
        return chunk

    def readinto(self, buf) -> int:
        chunk = self.read(len(buf))
        buf[: len(chunk)] = chunk
        return len(chunk)


def _open_remote_zip() -> zipfile.ZipFile:
    return zipfile.ZipFile(io.BufferedReader(_RangeReader(BULK_URL), buffer_size=1 << 20))


def _area_members(zf: zipfile.ZipFile, prefix: str) -> list[str]:
    members = sorted(
        n for n in zf.namelist()
        if os.path.basename(n).startswith(prefix) and n.endswith(".csv")
    )
    if len(members) < MIN_AREA_MEMBERS:
        raise RuntimeError(
            f"bulk ZIP holds only {len(members)} {prefix}*.csv members "
            f"(expected >= {MIN_AREA_MEMBERS}) — the export layout changed"
        )
    return members


def _write_member(source, schema: pa.Schema, writer) -> None:
    """Parse one CSV member into the streamed parquet, in record batches."""
    reader = pacsv.open_csv(
        source,
        read_options=_READ_OPTS,
        parse_options=_PARSE_OPTS,
        convert_options=_convert_opts(schema),
    )
    for batch in reader:
        if batch.num_rows:
            writer.write_table(pa.Table.from_batches([batch], schema=schema))


def _fetch_recorded(asset_id: str) -> None:
    """Stamp a successful fetch: the source signature, then the parse revision.

    Order matters — `record_source_signature` does its own load/save of the
    asset state, so the revision write must read it back afterwards.
    """
    record_source_signature(asset_id, BULK_URL)
    state = load_state(asset_id)
    state[_REVISION_KEY] = PARSE_REVISION
    save_state(asset_id, state)


def _is_fresh(asset_id: str) -> bool:
    """Skip the fetch only if the raw we already hold is BOTH current with the
    source and produced by the current parse."""
    return (
        load_state(asset_id).get(_REVISION_KEY) == PARSE_REVISION
        and source_unchanged(asset_id, BULK_URL)
        and raw_asset_exists(asset_id, "parquet")
    )


@transient_retry()
def _download_bulk_zip(dest_path: str) -> None:
    """Stream the full bulk ZIP to a local temp file (bounded memory)."""
    client = get_client()
    with client.stream("GET", BULK_URL, timeout=(30.0, 300.0)) as resp:
        resp.raise_for_status()
        with open(dest_path, "wb") as fh:
            for chunk in resp.iter_bytes(1 << 20):
                fh.write(chunk)


def fetch_values(node_id: str) -> None:
    """The observation corpus — needs ~every byte of the ZIP, so download it."""
    asset = node_id  # the runtime passes the spec id; it IS the asset name

    tmp = tempfile.NamedTemporaryFile(suffix=".zip", delete=False)
    tmp.close()
    try:
        _download_bulk_zip(tmp.name)
        with zipfile.ZipFile(tmp.name) as zf:
            members = _area_members(zf, "WID_data_")
            with raw_parquet_writer(asset, DATA_SCHEMA) as writer:
                for member in members:
                    with zf.open(member) as fh:
                        _write_member(fh, DATA_SCHEMA, writer)
    finally:
        os.unlink(tmp.name)

    _fetch_recorded(asset)


def fetch_variables(node_id: str) -> None:
    """Per-area variable metadata — 24MB of the ZIP, pulled by range reads."""
    asset = node_id

    zf = _open_remote_zip()
    members = _area_members(zf, "WID_metadata_")
    with raw_parquet_writer(asset, METADATA_SCHEMA) as writer:
        for member in members:
            _write_member(pa.BufferReader(zf.read(member)), METADATA_SCHEMA, writer)

    _fetch_recorded(asset)


def fetch_countries(node_id: str) -> None:
    """The area-code dictionary — one 4KB member, pulled by range reads."""
    asset = node_id

    zf = _open_remote_zip()
    table = pacsv.read_csv(
        pa.BufferReader(zf.read("WID_countries.csv")),
        read_options=_READ_OPTS,
        parse_options=_PARSE_OPTS,
        convert_options=_convert_opts(COUNTRY_SCHEMA),
    )
    save_raw_parquet(table.cast(COUNTRY_SCHEMA), asset)

    _fetch_recorded(asset)


DOWNLOAD_SPECS = [
    NodeSpec(id="world-inequality-database-values", fn=fetch_values, kind="download"),
    NodeSpec(id="world-inequality-database-variables", fn=fetch_variables, kind="download"),
    NodeSpec(id="world-inequality-database-countries", fn=fetch_countries, kind="download"),
]

# One artifact behind all three nodes, so one freshness signal: the ZIP's
# ETag/Last-Modified. WID publishes no release calendar; the observed cadence is
# roughly annual (~July), and the export is served with both validators.
MAINTAIN_SPECS = [
    MaintainSpec(
        asset_id=spec.id,
        description=(
            "Full bulk export refreshed roughly annually (~July); no published "
            f"release calendar. Freshness observed via ETag/Last-Modified on {BULK_URL}."
        ),
        check=_is_fresh,
    )
    for spec in DOWNLOAD_SPECS
]
