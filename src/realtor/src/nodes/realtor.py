"""Realtor.com Research housing-market data.

Source: Realtor.com publishes monthly residential housing-market metrics as
full-history CSVs on the public S3 bucket econdata.s3-us-west-2.amazonaws.com
(no auth). Two report families, each at several geography levels:

  Core inventory metrics  -> Country, State, Metro (CBSA), County, Zip
  Market Hotness index    -> Metro (CBSA), County, Zip

Each file is one monthly time series (one row per geography per month, history
from 2016-07) carrying level metrics alongside derivable _mm/_yy/_vs_us momentum
columns and a quality_flag. We re-fetch each file in full every run (stateless
full re-pull — the files are complete histories and there is no incremental /
delta query) and stream it straight to a gzipped CSV raw asset. The transform
then drops the momentum/quality columns, builds a DATE from month_date_yyyymm,
and casts the level metrics. The largest file (Core Zip ~800MB) is streamed to
disk to stay well under the spawn-subprocess memory ceiling.

License: Realtor.com Research data is free for public use with attribution.
"""

import httpx

from subsets_utils import (
    NodeSpec,
    get_client,
    raw_writer,
    transient_retry,
)

_BASE = "https://econdata.s3-us-west-2.amazonaws.com/Reports"

# spec entity_id -> (report family, S3 path). Geography is encoded in the id.
_FILES = {
    "core_country":  ("core", "Core/RDC_Inventory_Core_Metrics_Country_History.csv"),
    "core_state":    ("core", "Core/RDC_Inventory_Core_Metrics_State_History.csv"),
    "core_metro":    ("core", "Core/RDC_Inventory_Core_Metrics_Metro_History.csv"),
    "core_county":   ("core", "Core/RDC_Inventory_Core_Metrics_County_History.csv"),
    "core_zip":      ("core", "Core/RDC_Inventory_Core_Metrics_Zip_History.csv"),
    "hotness_metro":  ("hotness", "Hotness/RDC_Inventory_Hotness_Metrics_Metro_History.csv"),
    "hotness_county": ("hotness", "Hotness/RDC_Inventory_Hotness_Metrics_County_History.csv"),
    "hotness_zip":    ("hotness", "Hotness/RDC_Inventory_Hotness_Metrics_Zip_History.csv"),
}

# spec id ("realtor-core-state") -> full URL
_URLS = {
    f"realtor-{eid.replace('_', '-')}": f"{_BASE}/{path}"
    for eid, (_family, path) in _FILES.items()
}


# --- download -------------------------------------------------------------


@transient_retry(attempts=5)
def _download_csv_gz(asset: str, url: str) -> None:
    """Stream one Realtor.com history CSV to a gzipped raw asset.

    Streamed (not buffered) because the Zip-level files are hundreds of MB;
    httpx streaming keeps peak RSS to a single chunk. Uses the shared
    subsets_utils httpx client (default User-Agent, redirect following).
    """
    client = get_client()
    timeout = httpx.Timeout(connect=15.0, read=300.0, write=120.0, pool=60.0)
    with client.stream("GET", url, timeout=timeout) as resp:
        resp.raise_for_status()
        with raw_writer(asset, "csv.gz", mode="wb", compression="gzip") as f:
            for chunk in resp.iter_bytes(chunk_size=1 << 20):
                f.write(chunk)


def fetch_one(node_id: str) -> None:
    # The runtime passes the spec id; it is also the asset name to write.
    _download_csv_gz(node_id, _URLS[node_id])


DOWNLOAD_SPECS = [
    NodeSpec(id=spec_id, fn=fetch_one, kind="download")
    for spec_id in _URLS
]
