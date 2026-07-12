"""Download specs for SOCAT v2026 products.

SOCAT has two practical bulk surfaces for the accepted products: NCEI-hosted
CSV files for gridded data, and ERDDAP CSV exports for the trajectory tables.
Both are streamed to gzip-compressed CSV raw assets so transforms can scan them
directly without zip or NetCDF handling.
"""

from __future__ import annotations

import os
from datetime import datetime, timezone
from urllib.parse import quote

from subsets_utils import (
    MaintainSpec,
    NodeSpec,
    get_client,
    list_raw_fragments,
    raw_asset_exists,
    raw_writer,
    record_source_signature,
    source_unchanged,
)

_CHUNK_SIZE = 1 << 20
_FIRST_FULLDATA_YEAR = 1957
_FULLDATA_MAX_AGE_DAYS = 370
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
    if node_id == "socat-socat-v2026-fulldata":
        _fetch_fulldata_by_year(node_id)
        return

    url = _URLS[node_id]
    client = get_client()
    with client.stream("GET", url, timeout=(10.0, 900.0)) as response:
        response.raise_for_status()
        with raw_writer(node_id, "csv.gz", mode="wb", compression="gzip") as out:
            for chunk in response.iter_bytes(_CHUNK_SIZE):
                if chunk:
                    out.write(chunk)
        record_source_signature(node_id, url, response=response)


def _fetch_fulldata_by_year(node_id: str) -> None:
    """Fetch full trajectory observations as yearly ERDDAP fragments.

    A single unconstrained ERDDAP CSV stream is large enough to fail with
    incomplete chunked reads. Year fragments keep each response bounded while
    preserving one logical raw asset through the raw manifest.
    """
    current_year = datetime.now(timezone.utc).year
    done_this_run = {
        fragment
        for fragment, meta in list_raw_fragments(node_id, "csv.gz").items()
        if meta.get("run_id") == os.environ.get("RUN_ID", "unknown")
    }
    for year in range(_FIRST_FULLDATA_YEAR, current_year + 1):
        fragment = str(year)
        if fragment in done_this_run:
            continue
        start = f"{year}-01-01T00:00:00Z"
        end = f"{year + 1}-01-01T00:00:00Z"
        constraint = (
            f"&time%3E={quote(start, safe='')}"
            f"&time%3C{quote(end, safe='')}"
        )
        url = f"{_URLS[node_id]}?{constraint}"
        client = get_client()
        with client.stream("GET", url, timeout=(10.0, 900.0)) as response:
            response.raise_for_status()
            with raw_writer(
                node_id,
                "csv.gz",
                mode="wb",
                compression="gzip",
                fragment=fragment,
            ) as out:
                for chunk in response.iter_bytes(_CHUNK_SIZE):
                    if chunk:
                        out.write(chunk)


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
    if asset_id == "socat-socat-v2026-fulldata":
        return _fulldata_fragments_fresh(asset_id)

    url = _URLS[asset_id]
    if not raw_asset_exists(asset_id, "csv.gz", max_age_days=370):
        return False
    if "ncei.noaa.gov" in url:
        return source_unchanged(asset_id, url)
    return True


def _fulldata_fragments_fresh(asset_id: str) -> bool:
    fragments = list_raw_fragments(asset_id, "csv.gz")
    if not fragments:
        return False

    current_year = datetime.now(timezone.utc).year
    expected = {str(year) for year in range(_FIRST_FULLDATA_YEAR, current_year + 1)}
    if not expected.issubset(fragments):
        return False

    newest_allowed_age_s = _FULLDATA_MAX_AGE_DAYS * 24 * 60 * 60
    now = datetime.now(timezone.utc)
    for year in expected:
        fetched_at = fragments[year].get("fetched_at")
        if not fetched_at:
            return False
        fetched = datetime.fromisoformat(fetched_at.replace("Z", "+00:00"))
        if (now - fetched).total_seconds() > newest_allowed_age_s:
            return False
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
