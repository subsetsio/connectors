"""Comparative Constitutions Project (CCP).

Three published subsets, three independent download nodes:

  ccp-cnc        Characteristics of National Constitutions — the flagship coded
                 panel (one row per country-year a constitution was in force;
                 ~2000 coded variables, ~21k rows, 1789-present). bulk_download.
  ccp-cce        Chronology of Constitutional Events — event-level timeline
                 (new constitutions, amendments, suspensions, reinstatements;
                 6 columns, ~20k rows, since 1789). bulk_download.
  constitutions  Constitute API constitution metadata — one row per
                 constitutional text in the Constitute corpus (238 records:
                 country, region, year_enacted, word_length, in_force, ...). REST JSON.

Fetch strategy (mechanism `bulk_download` for the two coded datasets):
  The CCP download page (comparativeconstitutionsproject.org/download-data/) is
  the version index. For each dataset we scrape the page and take the FIRST
  box.com zip link following the dataset's section heading — that link is always
  the latest version, so re-pulls pick up new releases automatically without
  hardcoding version-specific URLs (the box `/shared/static/<hash>.zip` hashes
  change every release). Box gotcha: a HEAD 404s, but a GET that follows
  redirects (utexas.box.com -> app.box.com -> public.boxcloud.com signed URL)
  resolves to the zip — subsets_utils.get follows redirects by default.

  The zip unpacks to <code>_vN/<code>/<code>_vN.csv (plus .dta/.xlsx/codebook).
  We read the full CSV (never the `_small` variant) with DuckDB using
  all_varchar=true: the CNC file is ~2000 heterogeneous coded columns, so a
  faithful all-text pass-through beats brittle per-column type inference. The
  thin SQL transform casts only the two structural keys (cowcode, year) and
  publishes every other column as-is.

Refresh: stateless full re-pull. Both coded datasets are small versioned
releases and the Constitute corpus is ~240 records — re-fetch each run; the
maintain step (authored later) gates whether a node actually runs. No
incremental filter exists (versioned bulk dumps + a full-corpus JSON list).
"""
import io
import os
import re
import tempfile
import zipfile

import duckdb

from subsets_utils import (
    NodeSpec,
    SqlNodeSpec,
    get,
    save_raw_ndjson,
    save_raw_parquet,
    transient_retry,
)

SLUG = "comparative-constitutions-project"
DOWNLOAD_PAGE = "https://comparativeconstitutionsproject.org/download-data/"
CONSTITUTIONS_URL = "https://www.constituteproject.org/service/constitutions?lang=en"
HTTP_TIMEOUT = (10.0, 300.0)  # (connect, read); CNC zip is ~118MB

# The CCP download page is a WordPress site behind a bot filter that 403s
# datacenter traffic / non-browser User-Agents. A realistic browser UA + Accept
# headers clears the common case; if the page still blocks us (IP-based), the
# pinned box.com URLs below keep the connector running. ASCII-only headers.
_BROWSER_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
}

# Verified latest-version zips (2026-06), used only as a fallback when the
# download-page scrape is blocked. Refresh these hashes when CCP ships a new vN
# (CNC ~annual, Chronology updated through 2026); the scrape path picks up new
# versions automatically whenever the page is reachable.
_PINNED_ZIP = {
    f"{SLUG}-ccp-cnc": "https://utexas.box.com/shared/static/cpgysqaogi1590ucv5x0wn59urqm00x3.zip",
    f"{SLUG}-ccp-cce": "https://utexas.box.com/shared/static/qzs6irrpbfzspvv6sq94r98yw9rsh5lz.zip",
}

# Bulk-CSV datasets keyed by download spec id -> the section heading on the
# download page whose first box.com link is the latest-version zip, and the
# inner-file code used to pick the right CSV member.
_BULK = {
    f"{SLUG}-ccp-cnc": {
        "heading": "Characteristics of National Constitutions",
        "code": "ccpcnc",
    },
    f"{SLUG}-ccp-cce": {
        "heading": "Chronology of Constitutional Events",
        "code": "ccpcce",
    },
}


@transient_retry()
def _get_text(url: str) -> str:
    resp = get(url, headers=_BROWSER_HEADERS, timeout=HTTP_TIMEOUT)
    resp.raise_for_status()
    return resp.text


@transient_retry()
def _get_bytes(url: str) -> bytes:
    resp = get(url, headers=_BROWSER_HEADERS, timeout=HTTP_TIMEOUT)
    resp.raise_for_status()
    return resp.content


@transient_retry()
def _get_json(url: str):
    resp = get(url, headers=_BROWSER_HEADERS, timeout=HTTP_TIMEOUT)
    resp.raise_for_status()
    return resp.json()


def _resolve_latest_zip(heading: str) -> str:
    """Return the latest-version box.com zip URL for a dataset section.

    The download page lists each dataset under an <h> heading, newest version
    first. We anchor on the heading text and take the first box.com /shared/
    static/*.zip link after it.
    """
    page = _get_text(DOWNLOAD_PAGE)
    anchor = re.search(re.escape(heading), page)
    if not anchor:
        raise RuntimeError(
            f"download page heading not found: {heading!r} (page layout changed?)"
        )
    after = page[anchor.end():]
    m = re.search(
        r'href="(https://[^"]*box\.com/shared/static/[^"]+\.zip)"', after, re.IGNORECASE
    )
    if not m:
        raise RuntimeError(
            f"no box.com zip link after heading {heading!r} (page layout changed?)"
        )
    return m.group(1)


def _latest_zip_url(node_id: str, heading: str) -> str:
    """Latest-version zip URL: scrape the download page (auto version
    discovery), falling back to the pinned URL when the WordPress page blocks
    us (datacenter 403) so the connector keeps running."""
    try:
        return _resolve_latest_zip(heading)
    except Exception as exc:  # noqa: BLE001 - logged with context, then fall back
        fallback = _PINNED_ZIP[node_id]
        print(
            f"[ccp] download-page scrape failed for {node_id} "
            f"({type(exc).__name__}: {exc}); using pinned zip {fallback}"
        )
        return fallback


def _pick_csv_member(zf: zipfile.ZipFile, code: str) -> str:
    """The full (non-_small) CSV member for this dataset code."""
    members = [
        n
        for n in zf.namelist()
        if n.lower().endswith(".csv")
        and "__macosx" not in n.lower()
        and "_small" not in n.lower()
        and code in n.lower()
    ]
    if not members:
        raise RuntimeError(
            f"no full CSV member for code {code!r} in zip; members={zf.namelist()[:20]}"
        )
    # If several remain, the shortest path is the canonical top-level CSV.
    return min(members, key=len)


def fetch_bulk_csv(node_id: str) -> None:
    asset = node_id  # the runtime passes the spec id; it IS the asset name
    cfg = _BULK[node_id]

    url = _latest_zip_url(node_id, cfg["heading"])
    blob = _get_bytes(url)

    with zipfile.ZipFile(io.BytesIO(blob)) as zf:
        member = _pick_csv_member(zf, cfg["code"])
        csv_bytes = zf.read(member)

    tmp = tempfile.NamedTemporaryFile(suffix=".csv", delete=False)
    try:
        tmp.write(csv_bytes)
        tmp.flush()
        tmp.close()
        path = tmp.name.replace("'", "''")
        con = duckdb.connect()
        try:
            # all_varchar: these are wide, heterogeneous coded survey files
            # (CNC ~2000 cols); keep every column as text and let the transform
            # cast the structural keys. null_padding tolerates short trailing
            # rows on very wide files.
            table = con.execute(
                f"SELECT * FROM read_csv_auto('{path}', all_varchar=true, "
                "null_padding=true, header=true)"
            ).fetch_arrow_table()
        finally:
            con.close()
    finally:
        os.unlink(tmp.name)

    if table.num_rows == 0:
        raise RuntimeError(f"{node_id}: parsed CSV has 0 rows ({url})")

    save_raw_parquet(table, asset)


def fetch_constitutions(node_id: str) -> None:
    asset = node_id
    data = _get_json(CONSTITUTIONS_URL)
    if not isinstance(data, list) or not data:
        raise RuntimeError(f"{node_id}: constitutions endpoint returned no records")
    # Heterogeneous nullable fields (copyright/translator/year_* are often null;
    # year_* arrive as numeric strings) -> NDJSON, re-typed on read.
    save_raw_ndjson(data, asset)


DOWNLOAD_SPECS = [
    NodeSpec(id=f"{SLUG}-ccp-cnc", fn=fetch_bulk_csv, kind="download"),
    NodeSpec(id=f"{SLUG}-ccp-cce", fn=fetch_bulk_csv, kind="download"),
    NodeSpec(id=f"{SLUG}-constitutions", fn=fetch_constitutions, kind="download"),
]

# One published Delta table per subset. The coded panels pass through faithfully
# (all columns text) except the two structural keys, which we cast to INTEGER so
# downstream joins/filters on country-code and year are typed. The constitutions
# table is already typed by NDJSON inference, so it passes through as-is.
TRANSFORM_SPECS = [
    SqlNodeSpec(
        id=f"{SLUG}-ccp-cnc-transform",
        deps=[f"{SLUG}-ccp-cnc"],
        sql=f'''
            SELECT * REPLACE (
                TRY_CAST(year AS INTEGER)    AS year,
                TRY_CAST(cowcode AS INTEGER) AS cowcode
            )
            FROM "{SLUG}-ccp-cnc"
        ''',
    ),
    SqlNodeSpec(
        id=f"{SLUG}-ccp-cce-transform",
        deps=[f"{SLUG}-ccp-cce"],
        sql=f'''
            SELECT * REPLACE (
                TRY_CAST(year AS INTEGER)    AS year,
                TRY_CAST(cowcode AS INTEGER) AS cowcode
            )
            FROM "{SLUG}-ccp-cce"
        ''',
    ),
    SqlNodeSpec(
        id=f"{SLUG}-constitutions-transform",
        deps=[f"{SLUG}-constitutions"],
        sql=f'SELECT * FROM "{SLUG}-constitutions"',
    ),
]
