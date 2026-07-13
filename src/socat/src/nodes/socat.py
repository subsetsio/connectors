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
_FULLDATA_MAX_AGE_DAYS = 370
_FULLDATA_YEARS = (
    1957,
    1961,
    1962,
    1963,
    1968,
    1969,
    1970,
    1973,
    1974,
    1975,
    1976,
    1977,
    1978,
    1979,
    1980,
    1981,
    1982,
    1983,
    1984,
    1985,
    1986,
    1987,
    1988,
    1989,
    1990,
    1991,
    1992,
    1993,
    1994,
    1995,
    1996,
    1997,
    1998,
    1999,
    2000,
    2001,
    2002,
    2003,
    2004,
    2005,
    2006,
    2007,
    2008,
    2009,
    2010,
    2011,
    2012,
    2013,
    2014,
    2015,
    2016,
    2017,
    2018,
    2019,
    2020,
    2021,
    2022,
    2023,
    2024,
    2025,
    2026,
)
_FULLDATA_MONTHLY_FROM_YEAR = 2008
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
    """Fetch full trajectory observations as bounded ERDDAP fragments.

    A single unconstrained ERDDAP CSV stream is large enough to fail with
    incomplete chunked reads. Older low-volume years are fetched as yearly
    fragments; 2008+ is split monthly to keep high-volume responses bounded
    while preserving one logical raw asset through the raw manifest.
    """
    done_this_run = {
        fragment
        for fragment, meta in list_raw_fragments(node_id, "csv.gz").items()
        if meta.get("run_id") == os.environ.get("RUN_ID", "unknown")
    }
    for fragment, start, end in _fulldata_fragment_windows():
        if fragment in done_this_run:
            continue
        constraint = (
            f"&time%3E={quote(start, safe='')}"
            f"&time%3C{quote(end, safe='')}"
        )
        url = f"{_URLS[node_id]}?{constraint}"
        client = get_client()
        with client.stream("GET", url, timeout=(10.0, 900.0)) as response:
            if response.status_code == 404:
                body = response.read().decode("utf-8", errors="replace")
                if "nRows = 0" in body:
                    continue
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


def _fulldata_fragment_windows() -> tuple[tuple[str, str, str], ...]:
    windows: list[tuple[str, str, str]] = []
    for year in _FULLDATA_YEARS:
        if year < _FULLDATA_MONTHLY_FROM_YEAR:
            windows.append(
                (
                    str(year),
                    f"{year}-01-01T00:00:00Z",
                    f"{year + 1}-01-01T00:00:00Z",
                )
            )
            continue

        for month in range(1, 13):
            if month == 12:
                next_year = year + 1
                next_month = 1
            else:
                next_year = year
                next_month = month + 1
            windows.append(
                (
                    f"{year}-{month:02d}",
                    f"{year}-{month:02d}-01T00:00:00Z",
                    f"{next_year}-{next_month:02d}-01T00:00:00Z",
                )
            )
    return tuple(windows)


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

    expected = {fragment for fragment, _, _ in _fulldata_fragment_windows()}
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
