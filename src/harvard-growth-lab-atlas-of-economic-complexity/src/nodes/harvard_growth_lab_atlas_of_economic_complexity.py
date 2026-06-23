"""Harvard Growth Lab — Atlas of Economic Complexity.

Bulk per-file download from the Harvard Dataverse 'atlas' collection via the
native REST API (mechanism: dataverse_native). Each rank-active subset maps to
one Dataverse dataset (stable DOI) and a set of CSV files within it that share a
schema. Files split by year-range (the multi-GB bilateral tables) and by product
digit-level (1/2/4/6) are unioned into one raw asset; the digit level is carried
as a `product_level` column. Per-row queries don't exist, so every refresh is a
full re-pull (source updates ~annually, Apr-Jul) — the maintain step gates
whether a node runs. The largest constituent CSVs are ~5GB, so each file is
streamed CSV->parquet with bounded memory (never materialized whole).
"""

import io
import re

import pyarrow as pa
import pyarrow.csv as pacsv

from subsets_utils import (
    NodeSpec,
    SqlNodeSpec,
    get,
    get_client,
    raw_parquet_writer,
    transient_retry,
)
from constants import ENTITY_DOI, ENTITY_IDS

SLUG = "harvard-growth-lab-atlas-of-economic-complexity"
DATAVERSE = "https://dataverse.harvard.edu/api"
BLOCK = 1 << 25  # 32MB CSV read blocks -> bounded-memory streaming

# Column -> raw parquet type. Codes stay strings (preserve leading zeros);
# anything unlisted defaults to string.
INT64 = {"country_id", "partner_country_id", "product_id"}
INT32 = {"year", "product_level", "eci_rank_sitc", "eci_rank_hs92", "eci_rank_hs12"}
DOUBLE = {
    "export_value", "import_value", "global_market_share", "distance", "cog", "pci",
    "eci", "coi", "diversity", "growth_proj", "eci_sitc", "eci_hs92", "eci_hs12",
    "value_final", "value_exporter", "value_importer",
}

PCODE = {
    "hs92": "product_hs92_code",
    "hs12": "product_hs12_code",
    "hs22": "product_hs22_code",
    "sitc": "product_sitc_code",
    "services-unilateral": "product_services_unilateral_code",
}
CLASSES = ["services-unilateral", "hs92", "hs12", "hs22", "sitc"]


# --- catalog helpers --------------------------------------------------------

def _stem(label):
    for ext in (".csv", ".tab", ".tsv"):
        if label.lower().endswith(ext):
            return label[: -len(ext)]
    return label


def _schema_key(label):
    """Collapse a file label to its schema group (drop year-range split and
    product digit-level suffixes) — mirrors the collect grouping."""
    stem = _stem(label)
    stem = re.sub(r"_\d{4}_\d{4}$", "", stem)
    stem = re.sub(r"_\d$", "", stem)
    return stem


def _digit_level(label):
    m = re.search(r"_(\d)(?:_\d{4}_\d{4})?$", _stem(label))
    return m.group(1) if m else None


def _col_type(name):
    if name in INT64:
        return pa.int64()
    if name in INT32:
        return pa.int32()
    if name in DOUBLE:
        return pa.float64()
    return pa.string()


@transient_retry()
def _dataset_files(doi):
    resp = get(
        f"{DATAVERSE}/datasets/:persistentId/",
        params={"persistentId": f"doi:10.7910/DVN/{doi}"},
        timeout=(10.0, 120.0),
    )
    resp.raise_for_status()
    out = []
    for f in resp.json()["data"]["latestVersion"]["files"]:
        label = f["label"]
        if "data_dictionary" in label.lower():
            continue
        out.append((label, f["dataFile"]["id"]))
    return out


@transient_retry()
def _header(file_id):
    resp = get(
        f"{DATAVERSE}/access/datafile/{file_id}",
        headers={"Range": "bytes=0-16383"},
        timeout=(10.0, 120.0),
    )
    resp.raise_for_status()
    line = resp.content.split(b"\n", 1)[0].decode("utf-8", "replace").strip("\r")
    return line.split(",")


def _select_files(entity):
    """Return (file_id, label, digit_level) for every CSV belonging to this
    entity, by re-deriving the schema grouping from the live file listing."""
    doi = ENTITY_DOI[entity]
    match_key = entity[len("reported-"):] if entity.startswith("reported-") else entity
    out = []
    for label, fid in _dataset_files(doi):
        if _schema_key(label).replace("_", "-") == match_key:
            out.append((fid, label, _digit_level(label)))
    if not out:
        raise AssertionError(f"{entity}: no source files matched in doi {doi}")
    return out


# --- streaming CSV -> parquet ----------------------------------------------

class _HttpRaw(io.RawIOBase):
    """Adapt an httpx byte iterator to a readable stream for pyarrow."""

    def __init__(self, byte_iter):
        self._it = byte_iter
        self._buf = b""

    def readable(self):
        return True

    def readinto(self, b):
        if not self._buf:
            try:
                self._buf = next(self._it)
            except StopIteration:
                return 0
        n = min(len(b), len(self._buf))
        b[: n] = self._buf[:n]
        self._buf = self._buf[n:]
        return n


def _cast_batch(batch, schema, level):
    n = batch.num_rows
    present = set(batch.schema.names)
    arrays = []
    for field in schema:
        name = field.name
        if name == "product_level":
            arrays.append(pa.array([level] * n, type=pa.string()).cast(field.type))
        elif name in present:
            arrays.append(batch.column(name).cast(field.type))
        else:
            arrays.append(pa.nulls(n, field.type))
    return pa.RecordBatch.from_arrays(arrays, schema=schema)


@transient_retry()
def _build_asset(asset, files, schema, include_level):
    """Stream every constituent CSV into one parquet asset. Wrapped whole in
    retry: any mid-stream failure restarts from a fresh (truncating) writer, so
    a partial download never leaves duplicated rows behind."""
    read_opts = pacsv.ReadOptions(block_size=BLOCK)
    parse_opts = pacsv.ParseOptions(newlines_in_values=False)
    with raw_parquet_writer(asset, schema) as writer:
        for fid, label, level in files:
            cols = _header(fid)
            conv = pacsv.ConvertOptions(
                column_types={c: pa.string() for c in cols},
                strings_can_be_null=True,
            )
            lvl = level if include_level else None
            url = f"{DATAVERSE}/access/datafile/{fid}"
            client = get_client()
            with client.stream("GET", url, timeout=(10.0, 600.0)) as resp:
                resp.raise_for_status()
                stream = io.BufferedReader(_HttpRaw(resp.iter_bytes()), buffer_size=BLOCK)
                reader = pacsv.open_csv(
                    stream, read_options=read_opts, parse_options=parse_opts,
                    convert_options=conv,
                )
                while True:
                    try:
                        batch = reader.read_next_batch()
                    except StopIteration:
                        break
                    if batch.num_rows == 0:
                        continue
                    rb = _cast_batch(batch, schema, lvl)
                    writer.write_table(pa.Table.from_batches([rb], schema=schema))


def fetch_one(node_id: str) -> None:
    asset = node_id
    entity = node_id[len(SLUG) + 1:]
    files = _select_files(entity)

    # Build the typed superset schema (union of all constituent headers).
    cols = []
    for fid, _label, _lvl in files:
        for c in _header(fid):
            if c not in cols:
                cols.append(c)
    include_level = len({lvl for _f, _l, lvl in files if lvl}) >= 2
    fields = [(c, _col_type(c)) for c in cols]
    if include_level:
        fields.append(("product_level", pa.int32()))
    schema = pa.schema(fields)

    _build_asset(asset, files, schema, include_level)


DOWNLOAD_SPECS = [
    NodeSpec(id=f"{SLUG}-{eid}", fn=fetch_one, kind="download")
    for eid in ENTITY_IDS
]


# --- transforms: thin per-shape cast/rename --------------------------------

def _split_entity(entity):
    if entity == "growth-proj-eci-rankings":
        return ("growth", None, None)
    if entity.startswith("reported-"):
        rest = entity[len("reported-"):]
        return ("reported", rest.split("-")[0], "country-country-product-year")
    for c in CLASSES:
        if entity.startswith(c + "-"):
            return (c, c, entity[len(c) + 1:])
    raise AssertionError(f"unrecognized entity {entity}")


def _transform_sql(dep, entity):
    kind, cls, shape = _split_entity(entity)
    v = f'"{dep}"'

    if kind == "growth":
        return f"""
            SELECT country_id, country_iso3_code, year, growth_proj,
                   TRY_CAST(in_rankings AS BOOLEAN) AS in_rankings,
                   eci_sitc, eci_rank_sitc, eci_hs92, eci_rank_hs92,
                   eci_hs12, eci_rank_hs12
            FROM {v} WHERE year IS NOT NULL
        """

    if kind == "reported":
        return f"""
            SELECT year, exporter, importer,
                   commoditycode AS product_code,
                   value_final, value_exporter, value_importer
            FROM {v} WHERE year IS NOT NULL
        """

    pcode = PCODE[cls]
    if shape == "country-year":
        if cls == "services-unilateral":
            return f"""
                SELECT country_id, country_iso3_code, year,
                       export_value, import_value
                FROM {v} WHERE year IS NOT NULL
            """
        return f"""
            SELECT country_id, country_iso3_code, year,
                   export_value, import_value,
                   eci, coi, diversity, growth_proj
            FROM {v} WHERE year IS NOT NULL
        """
    if shape == "country-product-year":
        if cls == "services-unilateral":
            return f"""
                SELECT country_id, country_iso3_code, product_id,
                       {pcode} AS product_code, product_level, year,
                       export_value, import_value, global_market_share
                FROM {v} WHERE year IS NOT NULL
            """
        return f"""
            SELECT country_id, country_iso3_code, product_id,
                   {pcode} AS product_code, product_level, year,
                   export_value, import_value, global_market_share,
                   distance, cog, pci
            FROM {v} WHERE year IS NOT NULL
        """
    if shape == "product-year":
        return f"""
            SELECT product_id, {pcode} AS product_code, product_level, year,
                   export_value, import_value, pci
            FROM {v} WHERE year IS NOT NULL
        """
    if shape == "country-country-year":
        return f"""
            SELECT country_id, country_iso3_code,
                   partner_country_id, partner_iso3_code, year,
                   export_value, import_value
            FROM {v} WHERE year IS NOT NULL
        """
    if shape == "country-country-product-year":
        return f"""
            SELECT country_id, country_iso3_code,
                   partner_country_id, partner_iso3_code,
                   product_id, {pcode} AS product_code, year,
                   export_value, import_value
            FROM {v} WHERE year IS NOT NULL
        """
    raise AssertionError(f"unhandled shape {shape} for {entity}")


TRANSFORM_SPECS = [
    SqlNodeSpec(
        id=f"{s.id}-transform",
        deps=[s.id],
        sql=_transform_sql(s.id, s.id[len(SLUG) + 1:]),
    )
    for s in DOWNLOAD_SPECS
]
