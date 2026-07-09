"""Harvard Growth Lab - Atlas of Economic Complexity.

Bulk per-file download from the Harvard Dataverse `atlas` collection (mechanism
`dataverse_datafile`, enumerated via `dataverse_native`). Each entity is one
Dataverse dataset plus the files inside it that share a grain; the file ids are
resolved per run from the dataset's manifest because they change on republish.

Shape: stateless full re-pull. The access API has no `since`/cursor parameter and
no row-level filter, so a refresh re-fetches whole files. The accepted corpus is
~3 GB of CSV (the ~53 GB of bilateral-by-product detail was deferred at accept),
and the source republishes roughly annually, so a full pull is the right cost.

Raw layout: one parquet fragment per source CSV, all conforming to the entity's
union schema. Files within an entity do NOT all carry the same columns - product
depth 6 omits `export_rca`/`distance`/`cog`/`pci`, depth 1 and 2 omit
`export_rca` - so the union schema is computed from the live headers and absent
columns are written as nulls. Multi-depth entities gain a `product_level` column
recovered from the filename suffix, which the published files themselves do not
carry.

Two upstream quirks worth knowing:

  * `hs92_to_sitc3.csv` ships with only `target_sitc3,weight` - its source column
    is missing, so the rows cannot be attributed to an HS92 code. It is skipped
    with a loud warning rather than silently folded into the conversion table.
    (`sitc3_to_hs92.csv` covers the same pair in the other direction.)
  * The Product Space files write HS92 codes with leading zeros stripped
    (`101` where the classification table says `0101`). Codes are preserved
    verbatim as strings here; zero-padding is the transform stage's business.
"""

import io
import re

import pyarrow as pa
import pyarrow.csv as pacsv

from constants import ENTITIES, ENTITY_IDS
from subsets_utils import (
    NodeSpec,
    get,
    get_client,
    raw_parquet_writer,
    save_raw_parquet,
    transient_retry,
)

SLUG = "harvard-growth-lab-atlas-of-economic-complexity"
DATAVERSE = "https://dataverse.harvard.edu/api"
BLOCK = 1 << 24  # 16 MB CSV read blocks -> bounded-memory streaming

# The schema contract. Every column the Atlas publishes is typed here; an
# unlisted column is a schema change we want to hear about, not guess at.
# Classification codes stay strings - `0101` is not the integer 101.
COLUMN_TYPES: dict[str, pa.DataType] = {
    # identifiers
    "country_id": pa.int64(),
    "partner_country_id": pa.int64(),
    "product_id": pa.int64(),
    "product_parent_id": pa.int64(),
    "group_id": pa.int64(),
    "group_parent_id": pa.int64(),
    # codes and names
    "country_iso3_code": pa.string(),
    "partner_iso3_code": pa.string(),
    "country_name": pa.string(),
    "country_name_short": pa.string(),
    "group_type": pa.string(),
    "group_name": pa.string(),
    "product_name": pa.string(),
    "product_name_short": pa.string(),
    "product_id_hierarchy": pa.string(),
    "product_hs92_code": pa.string(),
    "product_hs12_code": pa.string(),
    "product_hs22_code": pa.string(),
    "product_sitc_code": pa.string(),
    "product_services_unilateral_code": pa.string(),
    "product_hs92_code_source": pa.string(),
    "product_hs92_code_target": pa.string(),
    "product_space_cluster_name": pa.string(),
    # dimensions
    "year": pa.int32(),
    "product_level": pa.int32(),
    # trade values (whole US dollars in every file observed)
    "export_value": pa.int64(),
    "import_value": pa.int64(),
    # complexity metrics
    "eci": pa.float64(),
    "coi": pa.float64(),
    "cog": pa.float64(),
    "pci": pa.float64(),
    "diversity": pa.int32(),
    "distance": pa.float64(),
    "export_rca": pa.float64(),
    "global_market_share": pa.float64(),
    "growth_proj": pa.float64(),
    "eci_sitc": pa.float64(),
    "eci_hs92": pa.float64(),
    "eci_hs12": pa.float64(),
    "eci_rank_sitc": pa.int32(),
    "eci_rank_hs92": pa.int32(),
    "eci_rank_hs12": pa.int32(),
    # product space
    "product_space_x": pa.float64(),
    "product_space_y": pa.float64(),
    # flags
    "in_rankings": pa.bool_(),
    "former_country": pa.bool_(),
    "show_feasibility": pa.bool_(),
    "natural_resource": pa.bool_(),
    "green_product": pa.bool_(),
}

# The uniform shape every conversion table is folded into.
CONVERSION_SCHEMA = pa.schema([
    ("source_classification", pa.string()),
    ("source_code", pa.string()),
    ("target_classification", pa.string()),
    ("target_code", pa.string()),
    ("weight", pa.float64()),
])

_LEVEL_SUFFIX = re.compile(r"_(\d)$")


# --- catalog ----------------------------------------------------------------

def _stem(filename: str) -> str:
    for ext in (".csv", ".tab", ".tsv"):
        if filename.lower().endswith(ext):
            return filename[: -len(ext)]
    return filename


def _product_level(filename: str) -> int | None:
    """Product digit-depth, recovered from the `_1`/`_2`/`_4`/`_6` suffix."""
    m = _LEVEL_SUFFIX.search(_stem(filename))
    return int(m.group(1)) if m else None


def _delimiter(filename: str) -> str:
    return "\t" if filename.lower().endswith((".tab", ".tsv")) else ","


@transient_retry()
def _dataset_files(doi: str) -> list[tuple[str, int]]:
    """(filename, dataFile_id) for the dataset's latest published version."""
    resp = get(
        f"{DATAVERSE}/datasets/:persistentId/versions/:latest",
        params={"persistentId": doi},
        timeout=(15.0, 120.0),
    )
    resp.raise_for_status()
    files = resp.json()["data"]["files"]
    return sorted(
        (f["dataFile"]["filename"], f["dataFile"]["id"])
        for f in files
        if "data_dictionary" not in f["dataFile"]["filename"].lower()
    )


def _entity_files(entity: str) -> list[tuple[str, int]]:
    spec = ENTITIES[entity]
    matched = [
        (name, fid) for name, fid in _dataset_files(spec["doi"])
        if name.startswith(spec["prefix"])
    ]
    if not matched:
        raise AssertionError(
            f"{entity}: no file in {spec['doi']} starts with {spec['prefix']!r} - "
            f"the source renamed its files"
        )
    return matched


@transient_retry()
def _header(file_id: int, delimiter: str) -> list[str]:
    """Column names, via a ranged GET - the multi-hundred-MB files must not be
    pulled just to read a header line."""
    resp = get(
        f"{DATAVERSE}/access/datafile/{file_id}",
        headers={"Range": "bytes=0-16383"},
        timeout=(15.0, 120.0),
    )
    resp.raise_for_status()
    line = resp.content.split(b"\n", 1)[0].decode("utf-8").strip("\r")
    return line.split(delimiter)


def _typed(columns: list[str]) -> dict[str, pa.DataType]:
    unknown = [c for c in columns if c not in COLUMN_TYPES]
    if unknown:
        raise AssertionError(
            f"undeclared column(s) {unknown} - the Atlas changed its schema; "
            f"add them to COLUMN_TYPES with an explicit type"
        )
    return {c: COLUMN_TYPES[c] for c in columns}


# --- streaming CSV -> parquet -----------------------------------------------

class _HttpRaw(io.RawIOBase):
    """Adapt an httpx byte iterator to a readable stream for pyarrow, so a
    multi-hundred-MB CSV is parsed as it arrives instead of buffered whole."""

    def __init__(self, byte_iter):
        self._it = byte_iter
        self._buf = b""

    def readable(self) -> bool:
        return True

    def readinto(self, b) -> int:
        while not self._buf:
            try:
                self._buf = next(self._it)
            except StopIteration:
                return 0
        n = min(len(b), len(self._buf))
        b[:n] = self._buf[:n]
        self._buf = self._buf[n:]
        return n


def _conform(batch: pa.RecordBatch, schema: pa.Schema, level: int | None) -> pa.RecordBatch:
    """Widen one CSV's batch to the entity's union schema: absent columns become
    nulls, and `product_level` is injected from the filename.

    The classification tables publish a real `product_level` column, so a present
    column always wins over the injected one.
    """
    present = set(batch.schema.names)
    arrays = []
    for field in schema:
        if field.name in present:
            arrays.append(batch.column(field.name))
        elif field.name == "product_level":
            arrays.append(pa.array([level] * batch.num_rows, type=field.type))
        else:
            arrays.append(pa.nulls(batch.num_rows, field.type))
    return pa.RecordBatch.from_arrays(arrays, schema=schema)


@transient_retry()
def _stream_file(asset: str, fragment: str | None, file_id: int, filename: str,
                 schema: pa.Schema, level: int | None) -> None:
    """Stream one source CSV into one parquet fragment of `asset`.

    Retry is scoped to the single file: a mid-stream blip re-downloads only this
    fragment (its writer is truncated and rebuilt) and leaves its siblings alone.
    """
    delimiter = _delimiter(filename)
    convert = pacsv.ConvertOptions(column_types=_typed(_header(file_id, delimiter)))
    read = pacsv.ReadOptions(block_size=BLOCK)
    parse = pacsv.ParseOptions(delimiter=delimiter, newlines_in_values=False)

    with raw_parquet_writer(asset, schema, fragment=fragment) as writer:
        with get_client().stream(
            "GET", f"{DATAVERSE}/access/datafile/{file_id}", timeout=(15.0, 600.0)
        ) as resp:
            resp.raise_for_status()
            stream = io.BufferedReader(_HttpRaw(resp.iter_bytes()), buffer_size=BLOCK)
            reader = pacsv.open_csv(stream, read_options=read,
                                    parse_options=parse, convert_options=convert)
            for batch in reader:
                if batch.num_rows:
                    writer.write_batch(_conform(batch, schema, level))


def _fetch_tabular(asset: str, entity: str) -> None:
    """The default layout: publish each source CSV as-is, under a union schema."""
    files = _entity_files(entity)
    levels = {_product_level(name) for name, _ in files}
    multi_depth = len(levels - {None}) > 1

    columns: list[str] = []
    for name, file_id in files:
        for col in _header(file_id, _delimiter(name)):
            if col not in columns:
                columns.append(col)
    fields = list(_typed(columns).items())
    if multi_depth:
        fields.append(("product_level", COLUMN_TYPES["product_level"]))
    schema = pa.schema(fields)

    # One source file -> a plain `<asset>.parquet`; several -> one fragment each,
    # named for the file it came from, which the dep view globs back together.
    for name, file_id in files:
        level = _product_level(name) if multi_depth else None
        fragment = _stem(name) if len(files) > 1 else None
        _stream_file(asset, fragment, file_id, name, schema, level)


# --- conversion tables ------------------------------------------------------

@transient_retry()
def _fetch_conversion_table(file_id: int, filename: str) -> pa.Table | None:
    """One (source -> target) classification mapping, reshaped to a uniform
    schema. The source and target classifications are read off the column names
    (`source_hs17`, `target_hs22`), not the filename - `hs92_hs96.tab` is named
    without the `_to_` the others use.

    Returns None for a file with no source column: `hs92_to_sitc3.csv` ships as
    `target_sitc3,weight`, so its rows cannot be attributed to a source code.
    """
    delimiter = _delimiter(filename)
    header = _header(file_id, delimiter)
    source = next((c for c in header if c.startswith("source_")), None)
    target = next((c for c in header if c.startswith("target_")), None)
    if source is None or target is None:
        print(f"  !! skipping {filename}: header {header} has no source/target pair")
        return None

    resp = get(f"{DATAVERSE}/access/datafile/{file_id}", timeout=(15.0, 600.0))
    resp.raise_for_status()
    table = pacsv.read_csv(
        io.BytesIO(resp.content),
        parse_options=pacsv.ParseOptions(delimiter=delimiter),
        convert_options=pacsv.ConvertOptions(
            column_types={source: pa.string(), target: pa.string(),
                          "weight": pa.float64()},
        ),
    )
    n = table.num_rows
    return pa.Table.from_arrays(
        [
            pa.array([source[len("source_"):]] * n, type=pa.string()),
            table.column(source),
            pa.array([target[len("target_"):]] * n, type=pa.string()),
            table.column(target),
            table.column("weight"),
        ],
        schema=CONVERSION_SCHEMA,
    )


def _fetch_conversion(asset: str, entity: str) -> None:
    """All 18 conversion tables folded into one asset, a fragment per pair.

    Each file is a few MB to 23 MB, so these are read whole rather than streamed.
    """
    kept = 0
    for name, file_id in _entity_files(entity):
        table = _fetch_conversion_table(file_id, name)
        if table is None:
            continue
        save_raw_parquet(table, asset, fragment=_stem(name))
        kept += 1
    if not kept:
        raise AssertionError(f"{entity}: every conversion table was unusable")


# --- specs ------------------------------------------------------------------

def fetch_one(node_id: str) -> None:
    asset = node_id
    entity = node_id[len(SLUG) + 1:]
    if ENTITIES[entity].get("layout") == "conversion":
        _fetch_conversion(asset, entity)
    else:
        _fetch_tabular(asset, entity)


DOWNLOAD_SPECS = [
    NodeSpec(id=f"{SLUG}-{entity}", fn=fetch_one, kind="download")
    for entity in ENTITY_IDS
]
