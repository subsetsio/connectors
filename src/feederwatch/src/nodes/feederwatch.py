"""Project FeederWatch connector.

Single citizen-science source (Cornell Lab of Ornithology + Birds Canada):
standardized bird counts at supplementary feeding stations across the US and
Canada since 1988. Access is bulk static CSV/ZIP on cdn.feederwatch.org.

Shape: stateless full re-pull. The whole corpus is a fixed set of bulk files
republished annually (~June 1); we re-fetch and overwrite every run, so late
corrections and the new season are picked up for free. No incremental filter
exists and none is needed.

URLs are point-in-time — both the path segment (e.g. 202406) and the filename
date stamp (May2024) increment each annual release — so we never hardcode them.
We resolve the current links at run time, then download the files themselves.

Link discovery: the entry page (feederwatch.org) is behind a Cloudflare managed
challenge that hard-403s datacenter IPs, so it is unreachable from the CI runner
even with browser headers. The data files, however, live on a *separate* host
(cdn.feederwatch.org = CloudFront + S3) which serves fine from anywhere. So we
discover the current link set from the most recent Wayback Machine snapshot of
the entry page (web.archive.org is reachable from CI and re-archives the page
within days of each annual release), then download the resolved CloudFront URLs
directly. We still try the live page first, in case it is ever reachable.

Three subsets:
  * observations        — the core checklist counts (7 year-range ZIPs, one
                          shared schema, streamed into one parquet).
  * site_descriptions   — per-site/per-period habitat & feeder attributes.
  * species_translation — the species codebook (code -> names + taxonomy).
"""

import io
import re
import zipfile

import pyarrow as pa
import pyarrow.csv as pacsv

from subsets_utils import (
    NodeSpec,
    get,
    configure_http,
    transient_retry,
    save_raw_parquet,
    raw_parquet_writer,
)

ENTRY_URL = "https://feederwatch.org/explore/raw-dataset-requests/"
ENTRY_TARGET = "feederwatch.org/explore/raw-dataset-requests/"  # for Wayback
WAYBACK_CDX = "https://web.archive.org/cdx/search/cdx"
WAYBACK_WEB = "https://web.archive.org/web"

# Any cdn.feederwatch.org data file URL. Used to scrape both the live HTML and
# the Wayback-rewritten HTML (where it appears embedded after the /web/<ts>/
# prefix), so the same pattern recovers the original CloudFront URL from both.
_CDN_LINK_RX = re.compile(
    r"https://cdn\.feederwatch\.org/data/[^\s\"'<>\\]+\.(?:zip|csv)"
)

# A full browser-like header set. Harmless on CloudFront/Wayback; lets us also
# try the live Cloudflare page on the off chance it is reachable. ASCII only.
_BROWSER_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
}

# Header is identical across all year-range files (verified 1988-1995,
# 2006-2010, 2021-2024). Read every column as string and let "NA"/"" be null;
# the transform does the typing. A fixed all-string schema keeps the streamed
# parquet contract stable across the 7 files and across annual releases.
OBS_COLUMNS = [
    "LOC_ID", "LATITUDE", "LONGITUDE", "SUBNATIONAL1_CODE", "ENTRY_TECHNIQUE",
    "SUB_ID", "OBS_ID", "Month", "Day", "Year", "PROJ_PERIOD_ID",
    "SPECIES_CODE", "alt_full_spp_code", "HOW_MANY", "PLUS_CODE", "VALID",
    "REVIEWED", "DAY1_AM", "DAY1_PM", "DAY2_AM", "DAY2_PM",
    "EFFORT_HRS_ATLEAST", "SNOW_DEP_ATLEAST", "Data_Entry_Method",
]
OBS_SCHEMA = pa.schema([(c, pa.string()) for c in OBS_COLUMNS])

_NULL_VALUES = ["NA", "na", "NaN", ""]


@transient_retry()
def _fetch(url: str):
    # Long read timeout: the year-range ZIPs are tens-to-hundreds of MB.
    resp = get(url, timeout=(10.0, 600.0))
    resp.raise_for_status()
    return resp


def _links_from_live() -> list[str]:
    """CDN links from the live entry page (usually 403 from a datacenter IP)."""
    html = _fetch(ENTRY_URL).text
    return sorted(set(_CDN_LINK_RX.findall(html)))


def _links_from_wayback() -> list[str]:
    """CDN links from the most recent usable Wayback snapshot of the entry page.

    Walk snapshots newest-first; some are JS-stubs / challenge captures with no
    links, so take the first snapshot that yields the full CloudFront link set.
    """
    cdx = _fetch(
        f"{WAYBACK_CDX}?url={ENTRY_TARGET}&output=json&fl=timestamp"
        f"&filter=statuscode:200&collapse=digest&limit=-40"
    ).json()
    # First row is the header (["timestamp"]); newest-first.
    timestamps = [row[0] for row in cdx[1:]][::-1]
    for ts in timestamps:
        html = _fetch(f"{WAYBACK_WEB}/{ts}/https://{ENTRY_TARGET}").text
        links = sorted(set(_CDN_LINK_RX.findall(html)))
        if links:
            return links
    raise RuntimeError(
        "no FeederWatch CDN links found in any recent Wayback snapshot of "
        f"{ENTRY_TARGET}"
    )


def _entry_links() -> list[str]:
    """All current cdn.feederwatch.org data links — live page, else Wayback."""
    try:
        links = _links_from_live()
        if links:
            return links
    except Exception as exc:  # Cloudflare 403 et al. — fall back to Wayback.
        print(f"  live entry page unavailable ({type(exc).__name__}: {exc}); "
              f"discovering links via Wayback Machine")
    return _links_from_wayback()


def _resolve_one(pattern: str) -> str:
    """Return the single discovered link matching `pattern`, else raise."""
    rx = re.compile(pattern)
    hits = sorted({u for u in _entry_links() if rx.search(u)})
    if not hits:
        raise RuntimeError(f"no FeederWatch link matched {pattern!r}")
    if len(hits) > 1:
        raise RuntimeError(f"expected one link for {pattern!r}, got {len(hits)}: {hits}")
    return hits[0]


def _read_csv_bytes(content: bytes) -> pa.Table:
    """Parse an in-memory CSV (NA -> null), inferring column types."""
    co = pacsv.ConvertOptions(null_values=_NULL_VALUES, strings_can_be_null=True)
    return pacsv.read_csv(io.BytesIO(content), convert_options=co)


def fetch_observations(node_id: str) -> None:
    configure_http(headers=_BROWSER_HEADERS)
    asset = node_id
    rx = re.compile(r"PFW_all_\d{4}_\d{4}_.*\.csv\.zip$")
    zips = sorted({u for u in _entry_links() if rx.search(u)})
    if not zips:
        raise RuntimeError(f"no observation ZIP links found on {ENTRY_URL}")

    read_opts = pacsv.ReadOptions(block_size=16 * 1024 * 1024)
    conv_opts = pacsv.ConvertOptions(
        column_types={c: pa.string() for c in OBS_COLUMNS},
        null_values=_NULL_VALUES,
        strings_can_be_null=True,
    )
    with raw_parquet_writer(asset, OBS_SCHEMA) as writer:
        for url in zips:
            resp = _fetch(url)
            zf = zipfile.ZipFile(io.BytesIO(resp.content))
            csv_name = next(
                (n for n in zf.namelist() if n.lower().endswith(".csv")), None
            )
            if csv_name is None:
                raise RuntimeError(f"no CSV inside {url}")
            with zf.open(csv_name) as f:
                reader = pacsv.open_csv(
                    f, read_options=read_opts, convert_options=conv_opts
                )
                for batch in reader:
                    # Enforce column order so every batch matches OBS_SCHEMA.
                    writer.write_batch(batch.select(OBS_COLUMNS))


def fetch_site_descriptions(node_id: str) -> None:
    configure_http(headers=_BROWSER_HEADERS)
    asset = node_id
    url = _resolve_one(r"PFW_count_site_data.*\.csv$")
    table = _read_csv_bytes(_fetch(url).content)
    save_raw_parquet(table, asset)


def fetch_species_translation(node_id: str) -> None:
    configure_http(headers=_BROWSER_HEADERS)
    asset = node_id
    url = _resolve_one(r"PFW_spp_translation_table.*\.csv$")
    table = _read_csv_bytes(_fetch(url).content)
    save_raw_parquet(table, asset)


DOWNLOAD_SPECS = [
    NodeSpec(id="feederwatch-observations", fn=fetch_observations, kind="download"),
    NodeSpec(id="feederwatch-site-descriptions", fn=fetch_site_descriptions, kind="download"),
    NodeSpec(id="feederwatch-species-translation", fn=fetch_species_translation, kind="download"),
]
