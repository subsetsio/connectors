"""Download specs for SOCAT v2026 products.

SOCAT has two practical bulk surfaces for the accepted products: NCEI-hosted
CSV files for gridded data, and ERDDAP CSV exports for the trajectory tables.
Both are streamed to gzip-compressed CSV raw assets so transforms can scan them
directly without zip or NetCDF handling.
"""

from __future__ import annotations

from subsets_utils import (
    MaintainSpec,
    NodeSpec,
    get_client,
    raw_asset_exists,
    raw_writer,
    record_source_signature,
    source_unchanged,
)

_CHUNK_SIZE = 1 << 20
_NCEI_GRID_BASE = (
    "https://www.ncei.noaa.gov/data/oceans/ncei/ocads/data/0315110/"
    "SOCATv2026_Gridded_Data"
)
_ERDDAP_TABLEDAP = "https://data.pmel.noaa.gov/socat/erddap/tabledap"

_URLS = {
    "socat-socat-v2026-fulldata": f"{_ERDDAP_TABLEDAP}/socat_v2026_fulldata.csv",
    "socat-socat-v2026-decimated": f"{_ERDDAP_TABLEDAP}/socat_v2026_decimated.csv",
    "socat-socat-v2026-qrtrdeg-gridded-coast-monthly": (
        f"{_NCEI_GRID_BASE}/SOCATv2026_qrtrdeg_gridded_coast_monthly.csv"
    ),
    "socat-socat-v2026-tracks-gridded-decadal": (
        f"{_NCEI_GRID_BASE}/SOCATv2026_tracks_gridded_decadal.csv"
    ),
    "socat-socat-v2026-tracks-gridded-yearly": (
        f"{_NCEI_GRID_BASE}/SOCATv2026_tracks_gridded_yearly.csv"
    ),
}


def fetch_csv(node_id: str) -> None:
    """Stream one SOCAT CSV product to raw storage."""
    url = _URLS[node_id]
    client = get_client()
    with client.stream("GET", url, timeout=(10.0, 900.0)) as response:
        response.raise_for_status()
        with raw_writer(node_id, "csv.gz", mode="wb", compression="gzip") as out:
            for chunk in response.iter_bytes(_CHUNK_SIZE):
                if chunk:
                    out.write(chunk)
        record_source_signature(node_id, url, response=response)


DOWNLOAD_SPECS = [
    NodeSpec(
        id="socat-socat-v2026-decimated",
        fn=fetch_csv,
        kind="download",
    ),
    NodeSpec(
        id="socat-socat-v2026-fulldata",
        fn=fetch_csv,
        kind="download",
    ),
    NodeSpec(
        id="socat-socat-v2026-qrtrdeg-gridded-coast-monthly",
        fn=fetch_csv,
        kind="download",
    ),
    NodeSpec(
        id="socat-socat-v2026-tracks-gridded-decadal",
        fn=fetch_csv,
        kind="download",
    ),
    NodeSpec(
        id="socat-socat-v2026-tracks-gridded-yearly",
        fn=fetch_csv,
        kind="download",
    ),
]


def _fresh_enough(asset_id: str) -> bool:
    url = _URLS[asset_id]
    if not raw_asset_exists(asset_id, "csv.gz", max_age_days=370):
        return False
    if "ncei.noaa.gov" in url:
        return source_unchanged(asset_id, url)
    return True


MAINTAIN_SPECS = [
    MaintainSpec(
        asset_id=spec.id,
        description=(
            "SOCAT publishes annual releases; raw assets are refreshed when "
            "older than 370 days, with NCEI Last-Modified/ETag validation "
            "where available."
        ),
        check=_fresh_enough,
    )
    for spec in DOWNLOAD_SPECS
]
