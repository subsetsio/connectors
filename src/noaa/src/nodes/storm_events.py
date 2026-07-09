"""NOAA storm-events — NWS Storm Events Database, per-year detail CSVs (gzip)
under the SWDI bulk directory.
"""

import csv
import gzip
import io
import re

import pyarrow as pa

from subsets_utils import raw_parquet_writer

from utils import NCEI, _get_bytes, _list_hrefs, _string_table

STORM_DIR = f"{NCEI}/pub/data/swdi/stormevents/csvfiles/"
_STORM_RE = re.compile(r"StormEvents_details-ftp_v1\.0_d(\d{4})_c\d+\.csv\.gz$")


def fetch_storm_events(node_id: str) -> None:
    asset = node_id
    files: dict[int, str] = {}
    for h in _list_hrefs(STORM_DIR):
        m = _STORM_RE.match(h)
        if m:
            files[int(m.group(1))] = h  # one detail file per year
    if len(files) < 60:
        raise RuntimeError(
            f"storm-events: only {len(files)} yearly detail files at {STORM_DIR}; "
            "listing shape likely changed"
        )
    years = sorted(files)

    # Header from the earliest file defines the (all-string) schema; later files
    # must match it exactly or we treat it as silent source drift.
    first = gzip.decompress(_get_bytes(STORM_DIR + files[years[0]])).decode("latin-1")
    first_reader = csv.reader(io.StringIO(first))
    header = next(first_reader)
    schema = pa.schema([(c, pa.string()) for c in header])

    total = 0
    dropped = 0
    with raw_parquet_writer(asset, schema) as w:
        tbl, d = _string_table(header, first_reader, schema)
        total += tbl.num_rows
        dropped += d
        w.write_table(tbl)
        for y in years[1:]:
            text = gzip.decompress(_get_bytes(STORM_DIR + files[y])).decode("latin-1")
            r = csv.reader(io.StringIO(text))
            h = next(r)
            if h != header:
                raise RuntimeError(f"storm-events {y}: header drift vs baseline")
            tbl, d = _string_table(header, r, schema)
            total += tbl.num_rows
            dropped += d
            w.write_table(tbl)
    if total < 100000:
        raise RuntimeError(f"storm-events: only {total} rows across {len(years)} years")
    if dropped > total // 1000:
        raise RuntimeError(f"storm-events: {dropped} malformed rows of {total + dropped}")

