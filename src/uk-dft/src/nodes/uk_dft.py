"""uk-dft — Department for Transport (UK) bulk statistical / reference tables.

The data.gov.uk CKAN catalog that the collect stage enumerated is, for DfT,
overwhelmingly HTML landing-page pointers (resources whose `format` is HTML
link to GOV.UK collection pages, not to data). Only a handful of DfT datasets
expose stable, machine-readable bulk tabular files. This connector builds those
four:

  * gb-road-traffic-counts      -> GB road traffic by local authority (1993-)
  * road-accidents-safety-data  -> STATS19 reported collisions (1979-latest)
  * naptan                       -> National Public Transport Access Nodes
  * nptg                         -> National Public Transport Gazetteer (localities)

Fetch shape: stateless full re-pull (shape 1). Every file is a full snapshot
with a stable URL and no incremental filter, so each run re-downloads the whole
table and the transform overwrites. Files are streamed to a scratch tempfile,
then parsed by DuckDB as **all-VARCHAR** into parquet — typing is deferred to
the SQL transform. This is deliberate: STATS19's combined collision file is
~1.5 GB of coded-integer columns with -1 sentinels, and letting the transform's
`read_csv_auto` infer types from a sample risks mis-detection that errors mid
scan. All-VARCHAR parquet is the stable contract; the transform casts.

No documented or observed rate limits on any host (per research). No auth.
"""

from __future__ import annotations

import os
import tempfile

import duckdb
import httpx

from subsets_utils import (
    NodeSpec,
    get_client,
    raw_parquet_writer,
    transient_retry,
)

SLUG = "uk-dft"

# entity_id -> fetch config. `url` is the stable bulk file; `read_opts` is
# extra DuckDB read_csv_auto args appended verbatim (rarely needed).
SOURCES = {
    "gb-road-traffic-counts": {
        # Local-authority level traffic (cars/taxis + all motor vehicles) by
        # year, GB-wide, 1993-latest. Clean wide CSV on GCS.
        "url": (
            "https://storage.googleapis.com/dft-statistics/road-traffic/"
            "downloads/data-gov-uk/local_authority_traffic.csv"
        ),
    },
    "road-accidents-safety-data": {
        # STATS19 reported personal-injury road collisions, full history
        # 1979-latest-published-year. One row per collision; coded columns.
        "url": (
            "https://data.dft.gov.uk/road-accidents-safety-data/"
            "dft-road-casualty-statistics-collision-1979-latest-published-year.csv"
        ),
    },
    "naptan": {
        # National Public Transport Access Nodes — every GB stop/station.
        "url": "https://naptan.api.dft.gov.uk/v1/access-nodes?dataFormat=csv",
    },
    "nptg": {
        # National Public Transport Gazetteer — localities reference table.
        "url": "https://naptan.api.dft.gov.uk/v1/nptg/localities",
    },
}


@transient_retry()
def _stream_to_file(url: str, path: str) -> None:
    """Stream a (potentially multi-GB) file to a local scratch path."""
    client = get_client()
    # (connect, read) — generous read timeout for the 1.5GB STATS19 file.
    with client.stream("GET", url, timeout=httpx.Timeout(30.0, read=600.0)) as resp:
        resp.raise_for_status()
        with open(path, "wb") as fh:
            for chunk in resp.iter_bytes(1 << 20):  # 1 MiB chunks
                fh.write(chunk)


def fetch_one(node_id: str) -> None:
    """Download one DfT bulk CSV and persist it as all-VARCHAR parquet.

    The runtime passes the spec id; it is also the asset name. The entity id is
    the id minus the ``uk-dft-`` prefix.
    """
    asset = node_id
    entity_id = node_id[len(SLUG) + 1:]
    cfg = SOURCES[entity_id]
    read_opts = cfg.get("read_opts", "")

    fd, tmp_path = tempfile.mkstemp(suffix=".csv")
    os.close(fd)
    try:
        _stream_to_file(cfg["url"], tmp_path)

        con = duckdb.connect()
        # all_varchar: defer all typing to the SQL transform (robust against
        # read_csv_auto mis-detecting coded columns on large files). The CSVs
        # all carry a header row.
        escaped = tmp_path.replace("'", "''")
        query = (
            f"SELECT * FROM read_csv_auto('{escaped}', "
            f"all_varchar=true, header=true{read_opts})"
        )
        reader = con.sql(query).fetch_record_batch()
        with raw_parquet_writer(asset, reader.schema) as writer:
            for batch in reader:
                if batch.num_rows:
                    writer.write_batch(batch)
        con.close()
    finally:
        try:
            os.remove(tmp_path)
        except OSError:
            pass


DOWNLOAD_SPECS = [
    NodeSpec(
        id=f"{SLUG}-{eid.lower().replace('_', '-')}",
        fn=fetch_one,
        kind="download",
    )
    for eid in SOURCES
]
