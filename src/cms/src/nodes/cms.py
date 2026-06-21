"""CMS connector — data.cms.gov open-data catalog + Provider Data Catalog (DKAN).

361 datasets across two sub-catalogs, each pulled as a single streamed bulk CSV
(the `bulk_csv_main` mechanism) rather than row-paginated — one request per
dataset keeps the run fast and gentle on the source (paginating the largest
datasets, ~28M rows, melted the server with 503s and could not finish in the
CI budget):

  * Main catalog (UUID ids) -> the data-api emits the full combined dataset as
    CSV in one shot:   GET /data-api/v1/dataset/{uuid}/data.csv
  * Provider Data Catalog (short/named ids) -> the DKAN datastore dumps the whole
    distribution as CSV: GET /provider-data/api/1/datastore/query/{id}/0/download?format=csv

Catalog scope is the queryable subset: collect drops the ~28 main datasets that
ship ONLY as ZIP bundles of yearly XLSX statistical reports ("CMS Program
Statistics", "MCBS COVID-19 Supplement", …) — they have no data-api/CSV
distribution (the data.csv endpoint hard-503s for them) and a multi-period
multi-sheet Excel bundle does not fit the one-clean-table-per-dataset model —
plus one verified-empty provider dataset (header-only CSV).

Stateless full re-pull each run (revisions picked up for free; no watermark
exists on the row data — catalogs expose only a dataset-level `modified` stamp a
later MaintainSpec can use to skip unchanged datasets).

Raw is written as all-string NDJSON, parsed with Python's lenient csv.reader.
CMS CSVs contain ragged rows and columns whose values drift type partway through
the file, so DuckDB's strict read_csv_auto (which the SQL transform would use on
a raw .csv) errors out on the large datasets; parsing to string NDJSON here and
letting the transform read_json_auto it back is robust. The transform is a thin
pass-through publishing one Delta table per dataset.
"""
import csv
import io
import json

import httpx

from subsets_utils import (
    NodeSpec,
    SqlNodeSpec,
    get_client,
    raw_writer,
    transient_retry,
)

MAIN_BASE = "https://data.cms.gov/data-api/v1/dataset"
PROV_BASE = "https://data.cms.gov/provider-data/api/1/datastore/query"
# Connect timeout, then a generous inter-chunk read timeout for multi-GB streams.
_TIMEOUT = httpx.Timeout(15.0, read=600.0)
_CHUNK = 1 << 20


class _ByteStream(io.RawIOBase):
    """Adapt an httpx byte-chunk iterator into a readable binary file object so
    csv.reader (via TextIOWrapper) can parse it streaming, bounded-memory, with
    correct handling of quoted fields that embed commas and newlines."""

    def __init__(self, chunks):
        self._it = iter(chunks)
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
        b[:n], self._buf = self._buf[:n], self._buf[n:]
        return n


@transient_retry(attempts=8, min_wait=5, max_wait=240)
def _download_to_ndjson(url: str, asset: str) -> int:
    """Stream one dataset's CSV, parse to all-string row dicts, write NDJSON.

    Retried as a whole: a mid-stream transient error re-downloads from scratch
    and overwrites (raw_writer truncates on open), so partial files never leak.
    """
    client = get_client()
    n = 0
    with client.stream("GET", url, timeout=_TIMEOUT) as resp:
        resp.raise_for_status()
        binary = io.BufferedReader(_ByteStream(resp.iter_bytes(_CHUNK)))
        text = io.TextIOWrapper(binary, encoding="utf-8", errors="replace", newline="")
        reader = csv.reader(text)
        header = next(reader, None)
        with raw_writer(asset, "ndjson.gz", mode="wt", compression="gzip") as out:
            if header is not None:
                width = len(header)
                for row in reader:
                    obj = {
                        header[i]: (row[i] if i < len(row) else None)
                        for i in range(width)
                    }
                    out.write(json.dumps(obj, separators=(",", ":")))
                    out.write("\n")
                    n += 1
    return n


def fetch_one(node_id: str) -> None:
    """Fetch one dataset (main or provider) as bulk CSV and stream it to NDJSON."""
    entity = _SPEC_TO_ENTITY[node_id]
    if entity in _MAIN_SET:
        url = f"{MAIN_BASE}/{entity}/data.csv"
    else:
        url = f"{PROV_BASE}/{entity}/0/download?format=csv"
    n = _download_to_ndjson(url, node_id)
    print(f"{node_id}: wrote {n:,} rows")


from constants import MAIN_IDS

from constants import PROVIDER_IDS

ENTITY_IDS = MAIN_IDS + PROVIDER_IDS
_MAIN_SET = set(MAIN_IDS)
# spec id -> original catalog entity id (lossless reverse of the id transform)
_SPEC_TO_ENTITY = {
    f"cms-{eid.lower().replace('_', '-')}": eid for eid in ENTITY_IDS
}

DOWNLOAD_SPECS = [
    NodeSpec(
        id=f"cms-{eid.lower().replace('_', '-')}",
        fn=fetch_one,
        kind="download",
    )
    for eid in ENTITY_IDS
]

# One published Delta table per dataset. Each dataset has its own column set, so
# the transform is an honest pass-through over the NDJSON view (read_json_auto
# yields VARCHAR columns straight from the published CSV values).
TRANSFORM_SPECS = [
    SqlNodeSpec(
        id=f"{s.id}-transform",
        deps=[s.id],
        sql=f'SELECT * FROM "{s.id}"',
    )
    for s in DOWNLOAD_SPECS
]
