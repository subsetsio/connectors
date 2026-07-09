"""UNICEF Indicator Data Warehouse connector (SDMX 2.1).

One download per in-scope dataflow: the full SDMX-CSV table is streamed from
the public warehouse and normalized to a uniform tidy long schema (universal
observation fields + a `dimensions` JSON blob preserving every other
disaggregation the dataflow carries).

Access: https://sdmx.data.unicef.org/ws/public/sdmxapi/rest/data/{agency},{flow},{version}/?format=csv
No auth. Full-corpus re-pull each refresh (stateless) — SDMX supports
`updatedAfter` for deltas but our pattern is whole-source snapshots and the
warehouse is small enough (largest flows ~hundreds of MB) to re-pull. Rows are
streamed to disk so memory stays bounded regardless of flow size.
"""
import codecs
import csv
import json
import re
import zlib

import pyarrow as pa

from constants import ENTITY_IDS
from subsets_utils import (
    NodeSpec,
    get_client,
    raw_parquet_writer,
    transient_retry,
)

BASE = "https://sdmx.data.unicef.org/ws/public/sdmxapi/rest/data"

# Rows are streamed to parquet in fixed-size batches so memory stays bounded
# regardless of flow size (the largest flows exceed 8M observations).
_BATCH_ROWS = 50_000

# Uniform tidy schema for every dataflow. All values are strings as they arrive
# in SDMX-CSV; the transform TRY_CASTs the numeric ones. Parquet (columnar,
# compressed, streamable by DuckDB) keeps transform memory far below the JSON
# parse spike that NDJSON incurs on the multi-million-row flows.
_FIELDS = [
    "ref_area", "ref_area_name", "indicator", "indicator_name",
    "sex", "age", "time_period", "obs_value", "unit_measure",
    "obs_status", "data_source", "lower_bound", "upper_bound", "dimensions",
]
SCHEMA = pa.schema([(f, pa.string()) for f in _FIELDS])


def _spec_id(entity_id: str) -> str:
    return "unicef-" + entity_id.lower().replace("_", "-")


# Header-name aliases for the universal tidy columns, in priority order. SDMX-CSV
# emits a code column (UPPER_CASE) immediately followed by a human-label column.
# UNICEF-agency flows use the standard SDMX names; the partner and country-office
# agencies each name their concepts differently (CD2030 prefixes everything `CD`,
# CAP2030 uses COUNTRY/UNITS/SOURCE, EMOPS/COVID use a bespoke indicator
# dimension), so every alias below is a concept the tidy schema promotes.
_ALIASES = {
    "ref_area": ("REF_AREA", "COUNTRY", "CDAREAS", "SUBREGION"),
    "ref_area_name": ("Geographic area", "Reference area", "Reference Areas",
                      "Country", "Areas", "Subregion"),
    "indicator": ("INDICATOR", "SERIES", "UNICEF_INDICATOR", "SITREP_INDICATOR",
                  "CDCOVERAGEINDICATORS", "CDDDEMINDICS", "CDDRIVERINDICATORS",
                  "CDT2INDICS"),
    "indicator_name": ("Indicator", "SDG Series", "Series Name",
                       "Situation Report Indicator", "Coverage indicators",
                       "Demographic indicators", "Driver indicators",
                       "Tier 2 indicators"),
    "sex": ("SEX", "CDGENDER"),
    "age": ("AGE", "AGE_GROUP", "CURRENT_AGE", "CDAGE"),
    "time_period": ("TIME_PERIOD",),
    "obs_value": ("OBS_VALUE",),
    "unit_measure": ("UNIT_MEASURE", "UNITS", "CDUNIT"),
    "obs_status": ("OBS_STATUS",),
    "data_source": ("DATA_SOURCE", "CDDATASOURCE", "SOURCE"),
    "lower_bound": ("LOWER_BOUND",),
    "upper_bound": ("UPPER_BOUND",),
}

# A code column is UPPER_SNAKE; label columns are human-cased. Any code column not
# consumed by a tidy field above is preserved in the `dimensions` JSON blob —
# which ones those are depends on the flow, so the exclusion set is computed per
# row rather than hardcoded (SUBREGION is the geography in PARAGUAY but an extra
# stratifier in CD2030:CD2030, and must survive in the blob there).
_CODE_COL = re.compile(r"^[A-Z][A-Z0-9_]*$")


def _first(row_by_header: dict, names) -> tuple[str | None, str | None]:
    """The first present alias as (header, value); (None, None) if none match."""
    for n in names:
        v = row_by_header.get(n)
        if v not in (None, ""):
            return (n, v)
    return (None, None)


def _normalize(header: list[str], values: list[str]) -> dict:
    """Map one SDMX-CSV row to the uniform tidy record."""
    d = {}
    for h, v in zip(header, values):
        if h not in d:  # keep first occurrence of a header
            d[h] = v
    rec = {}
    used = set()
    for field, names in _ALIASES.items():
        h, v = _first(d, names)
        rec[field] = v
        if h is not None:
            used.add(h)
    # Preserve every remaining code dimension/attribute as a JSON blob.
    dims = {
        h: v
        for h, v in d.items()
        if v not in (None, "") and _CODE_COL.match(h) and h not in used
    }
    rec["dimensions"] = json.dumps(dims, ensure_ascii=False) if dims else None
    return rec


def _flush(writer, batch: list[dict]) -> None:
    writer.write_table(pa.Table.from_pylist(batch, schema=SCHEMA))


def _decompressor(head: bytes):
    """A decompressobj matching what `head` actually is, or None for plain bytes."""
    if head[:2] == b"\x1f\x8b":
        return zlib.decompressobj(16 + zlib.MAX_WBITS)  # gzip
    if head[:1] == b"\x78":
        return zlib.decompressobj()                     # zlib-wrapped deflate
    return None


def _iter_lines(resp) -> "Iterator[str]":
    """Decoded text lines from the raw response body.

    The warehouse's `Vary` omits `Accept-Encoding`, so its fronting cache can
    return a `Content-Encoding: gzip` header on a body that was stored
    uncompressed (and the reverse). Trusting the header there fails the largest
    flows with a zlib "incorrect header check"; sniff the bytes instead. A
    stream that ends mid-member raises, so a truncated pull retries rather than
    silently writing a short table.
    """
    decomp = _decompressor(b"")
    sniffed = False
    text = codecs.getincrementaldecoder("utf-8")("replace")
    tail = ""
    for chunk in resp.iter_raw():
        if not chunk:
            continue
        if not sniffed:
            decomp, sniffed = _decompressor(chunk), True
        while decomp is not None:
            data = decomp.decompress(chunk)
            rest = decomp.unused_data  # a concatenated multi-member gzip stream
            chunk = data
            if not rest:
                break
            decomp = _decompressor(rest)
            if decomp is None:
                chunk += rest
                break
            chunk += decomp.decompress(rest)
            break
        if not chunk:
            continue
        # Split on \n only: str.splitlines would also break on \x0b/ ,
        # which SDMX labels are free to contain. Terminators are kept so
        # csv.reader can rejoin quoted fields that span lines.
        parts = (tail + text.decode(chunk)).split("\n")
        tail = parts.pop()
        yield from (p + "\n" for p in parts)
    if decomp is not None and not decomp.eof:
        raise ValueError("compressed response ended mid-stream (truncated)")
    tail += text.decode(b"", True)
    if tail:
        yield tail


@transient_retry()
def _stream_csv_to_parquet(url: str, asset: str) -> int:
    """Stream the dataflow CSV and write normalized parquet. Returns row count."""
    client = get_client()
    written = 0
    with client.stream(
        "GET",
        url,
        params={"format": "csv"},
        headers={"Accept-Encoding": "gzip"},
        timeout=(10.0, 600.0),
    ) as resp:
        resp.raise_for_status()
        reader = csv.reader(_iter_lines(resp))
        header = next(reader, None)
        if not header:
            return 0
        with raw_parquet_writer(asset, SCHEMA) as writer:
            batch: list[dict] = []
            for values in reader:
                if not values:
                    continue
                batch.append(_normalize(header, values))
                written += 1
                if len(batch) >= _BATCH_ROWS:
                    _flush(writer, batch)
                    batch = []
            if batch:
                _flush(writer, batch)
    return written


def fetch_one(node_id: str) -> None:
    asset = node_id  # the spec id IS the asset name
    # Recover the source entity (AGENCY:FLOW:VERSION) from the spec id.
    entity = next((e for e in ENTITY_IDS if _spec_id(e) == node_id), None)
    if entity is None:
        raise ValueError(f"no entity union member maps to spec id {node_id!r}")
    agency, flow, version = entity.split(":")
    url = f"{BASE}/{agency},{flow},{version}/"
    n = _stream_csv_to_parquet(url, asset)
    if n == 0:
        raise ValueError(f"{asset}: dataflow {entity} returned 0 observations")


DOWNLOAD_SPECS = [
    NodeSpec(id=_spec_id(eid), fn=fetch_one, kind="download")
    for eid in ENTITY_IDS
]
