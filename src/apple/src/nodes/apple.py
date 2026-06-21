"""Apple Marketing Tools (RSS) chart connector.

Mechanism: the public, unauthenticated v2 RSS Marketing Tools JSON feeds
(`rss.marketingtools.apple.com/api/v2/{storefront}/{media}/{feed_type}/{limit}/{result_type}.json`).
One request returns a full chart (up to 100 entries, no pagination). There is
no incremental/`since` query and the API returns ONLY the current snapshot, so
the correct shape is a **stateless full re-pull** every run: re-fetch the whole
cross-storefront corpus for each media and overwrite. The published time series
is built downstream by snapshotting daily (each run captures `feed.updated`).

One download node per media (apps, audio-books, books, music, podcasts). Each
node sweeps every storefront x feed_type for its media and writes one long-format
NDJSON raw asset: one row per (snapshot_date, storefront, feed_type, rank, entry).
Storefront / feed_type / rank are dimension columns, NOT separate datasets.

NDJSON (not parquet) because entries are heterogeneous across media (artistId /
artistUrl / contentAdvisoryRating / releaseDate come and go) and each carries a
nested `genres` list — exactly the drifty/nested shape the format rubric routes
to NDJSON.

Pacing: Apple documents no rate limit, but bursts get 503s. We self-limit to a
polite ~50 req/min and lean on exponential backoff for transient 503/500/5xx.
Invalid storefronts return 500 (ambiguous with a transient hiccup), so we drive a
curated storefront list and skip any storefront whose request fails permanently
(after retries) rather than failing the whole media node — a per-storefront unit
failure stays per-storefront. A media that collects zero rows, or skips more than
half its storefronts, raises loudly (signals a systemic outage / format change).
"""
from __future__ import annotations

from email.utils import parsedate_to_datetime

import httpx
from ratelimit import limits, sleep_and_retry

from subsets_utils import (
    NodeSpec,
    SqlNodeSpec,
    get,
    save_raw_ndjson,
    transient_retry,
)

BASE_URL = "https://rss.marketingtools.apple.com/api/v2"
CHART_LIMIT = 100  # max entries per chart; the API caps here

# Per-media fetch config: the result_type path segment and the valid feed_types.
# Verified live against the source — feed_types that 404 for the chosen
# result_type (e.g. music new-releases/coming-soon, which are albums-only) are
# excluded so we never request a known-invalid combo.
MEDIA_CONFIG = {
    "apps":        {"result_type": "apps",        "feed_types": ["top-free", "top-paid"]},
    "audio-books": {"result_type": "audio-books", "feed_types": ["top"]},
    "books":       {"result_type": "books",       "feed_types": ["top-free", "top-paid"]},
    "music":       {"result_type": "songs",       "feed_types": ["most-played"]},
    "podcasts":    {"result_type": "podcasts",    "feed_types": ["top"]},
}

# Curated Apple App Store storefronts (ISO 3166-1 alpha-2, lowercase). Apple
# publishes no machine-readable storefront index; this is the stable known set.
# Any code Apple has retired returns a permanent error and is skipped at runtime,
# so the list staying a touch broad than reality is harmless.
from constants import STOREFRONTS


@sleep_and_retry
@limits(calls=50, period=60)  # polite ~50/min; Apple documents no hard limit
def _rate_limited_get(url: str) -> httpx.Response:
    return get(url, timeout=(10.0, 120.0))


@transient_retry()
def _fetch_chart(url: str) -> dict:
    resp = _rate_limited_get(url)
    resp.raise_for_status()  # inside the retry so 5xx/429 are retried
    return resp.json()


def _parse_snapshot_date(feed_updated: str) -> str:
    """feed.updated e.g. 'Mon, 15 Jun 2026 16:35:38 +0000' -> 'YYYY-MM-DD'.

    A parse failure means the feed format changed (a bug) — let it raise.
    """
    return parsedate_to_datetime(feed_updated).date().isoformat()


def _rows_from_feed(feed: dict, storefront: str, media: str, feed_type: str) -> list[dict]:
    feed_updated = feed.get("updated")
    snapshot_date = _parse_snapshot_date(feed_updated)
    rows = []
    for rank, entry in enumerate(feed.get("results", []), start=1):
        genres = entry.get("genres") or []
        rows.append({
            "snapshot_date": snapshot_date,
            "feed_updated": feed_updated,
            "storefront": storefront,
            "media": media,
            "feed_type": feed_type,
            "rank": rank,
            "entity_id": entry.get("id"),
            "name": entry.get("name"),
            "artist_name": entry.get("artistName"),
            "artist_id": entry.get("artistId"),
            "artist_url": entry.get("artistUrl"),
            "kind": entry.get("kind"),
            "release_date": entry.get("releaseDate"),
            "content_advisory_rating": entry.get("contentAdvisoryRating"),
            "genre_names": [g.get("name") for g in genres if g.get("name")],
            "artwork_url": entry.get("artworkUrl100"),
            "url": entry.get("url"),
        })
    return rows


def fetch_media(node_id: str) -> None:
    """Sweep every storefront x feed_type for one media; write one NDJSON asset.

    Stateless full re-pull: the source only exposes the current snapshot, so we
    re-fetch the whole corpus each run and overwrite. The maintain step (later)
    decides whether this runs at all — if invoked, we fetch.
    """
    asset = node_id                       # the spec id IS the asset name
    media = node_id[len("apple-"):]       # recover the media from the id
    config = MEDIA_CONFIG[media]
    result_type = config["result_type"]
    feed_types = config["feed_types"]

    rows: list[dict] = []
    attempted = 0
    skipped = 0
    for storefront in STOREFRONTS:
        for feed_type in feed_types:
            attempted += 1
            url = f"{BASE_URL}/{storefront}/{media}/{feed_type}/{CHART_LIMIT}/{result_type}.json"
            try:
                data = _fetch_chart(url)
            except httpx.HTTPStatusError as exc:
                # 404 (combo not offered in this storefront) or a 5xx that
                # survived all retries (commonly an invalid/retired storefront,
                # which returns 500). Treat as a per-storefront skip, not a
                # whole-node failure.
                skipped += 1
                print(f"skip {storefront}/{media}/{feed_type}: "
                      f"HTTP {exc.response.status_code} {url}")
                continue
            rows.extend(_rows_from_feed(data["feed"], storefront, media, feed_type))

    # Safety caps that RAISE (never silently return a thin asset): a systemic
    # outage or a source-wide format change should fail loudly, not publish a
    # gutted chart.
    if not rows:
        raise RuntimeError(f"{asset}: 0 rows collected across {attempted} requests")
    if skipped > attempted / 2:
        raise RuntimeError(
            f"{asset}: {skipped}/{attempted} requests skipped — systemic failure")

    save_raw_ndjson(rows, asset)


DOWNLOAD_SPECS = [
    NodeSpec(id="apple-apps",        fn=fetch_media, kind="download"),
    NodeSpec(id="apple-audio-books", fn=fetch_media, kind="download"),
    NodeSpec(id="apple-books",       fn=fetch_media, kind="download"),
    NodeSpec(id="apple-music",       fn=fetch_media, kind="download"),
    NodeSpec(id="apple-podcasts",    fn=fetch_media, kind="download"),
]


def _transform_sql(view: str) -> str:
    # Thin parse-and-type pass: the raw NDJSON keys are already snake_case, so we
    # just cast, order the columns, and drop entries missing the natural key.
    return f'''
        SELECT
            CAST(snapshot_date AS DATE)        AS snapshot_date,
            CAST(feed_updated AS VARCHAR)      AS feed_updated,
            CAST(storefront AS VARCHAR)        AS storefront,
            CAST(media AS VARCHAR)             AS media,
            CAST(feed_type AS VARCHAR)         AS feed_type,
            CAST(rank AS INTEGER)              AS rank,
            CAST(entity_id AS VARCHAR)         AS entity_id,
            CAST(name AS VARCHAR)              AS name,
            CAST(artist_name AS VARCHAR)       AS artist_name,
            CAST(artist_id AS VARCHAR)         AS artist_id,
            CAST(artist_url AS VARCHAR)        AS artist_url,
            CAST(kind AS VARCHAR)              AS kind,
            CAST(release_date AS VARCHAR)      AS release_date,
            CAST(content_advisory_rating AS VARCHAR) AS content_advisory_rating,
            genre_names,
            CAST(artwork_url AS VARCHAR)       AS artwork_url,
            CAST(url AS VARCHAR)               AS url
        FROM "{view}"
        WHERE entity_id IS NOT NULL
    '''


TRANSFORM_SPECS = [
    SqlNodeSpec(
        id=f"{s.id}-transform",
        deps=[s.id],
        sql=_transform_sql(s.id),
    )
    for s in DOWNLOAD_SPECS
]
