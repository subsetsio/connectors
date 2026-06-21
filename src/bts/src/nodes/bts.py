"""BTS (Bureau of Transportation Statistics) — TranStats connector.

One download spec per TranStats data table (the rank-accepted entity union).
Each table is partitioned on the source by time period (monthly, quarterly, or
annual). Two download surfaces are used, both documented in research:

* **prezip** (preferred, used for the high-volume aviation tables that publish
  pre-zipped full-table snapshots): one stable ``/PREZIP/<prefix>_<year>_<period>.zip``
  per period. The ``<prefix>`` is discovered at runtime by issuing the site's
  prezip postback and reading the redirect target — never hardcoded.
* **custom download** (the generic fallback for every table without a prezip
  surface): an ASP.NET form POST to ``DL_SelectFields.aspx`` with ``chkAllVars``
  selected, which returns a zip containing one data CSV for that period.

Both surfaces deliver one CSV per period. The fetch fn is a **firehose** over a
table's periods: each period is written as its own NDJSON batch
(``bts-<code>-<batch_key>``) and the per-table watermark (count of periods
ingested) is saved after every batch, so a supervisor interrupt resumes cleanly.
A small overlap re-fetches the most recent periods each run to absorb revisions.

Raw is written as **NDJSON with string cell values** — lossless (no code/type
corruption) and drift-safe: column sets change across decades for some tables,
and ``read_json_auto`` unions batch files by name. Each row is stamped with an
injected ``obs_date`` / ``obs_year`` / ``obs_period`` derived from the period
being fetched, giving every published subset a uniform typed time dimension
regardless of which time columns the source CSV happens to carry.

The full corpus is large (decades of monthly flight-level data); there is no
``since``/cursor filter on the source, so partitioning *is* the incremental
unit and the firehose drains forward across supervisor-bounded runs.
"""
from __future__ import annotations

import csv
import html as htmlmod
import io
import json
import re
import zipfile

import httpx

from subsets_utils import (
    NodeSpec,
    SqlNodeSpec,
    get,
    post,
    load_state,
    save_state,
    raw_writer,
    transient_retry,
)

STATE_VERSION = 1

# Re-fetch this many of the most recently ingested periods each run to absorb
# source revisions (BTS revises recent months/quarters). Duplicates are dropped
# downstream; this is the safety, not a bug.
OVERLAP_PERIODS = 2

# The rank-accepted entity union (TranStats obfuscated table codes).
from constants import ENTITY_IDS

# Tables that publish a /PREZIP/ surface (probed). All others use the generic
# custom-download surface. The exact prezip filename prefix is still discovered
# at runtime — this set only routes which surface a table uses.
PREZIP_TABLES = {"FGJ", "FGK", "FHK", "FKF", "FLM"}

_GET_PAGE = "https://www.transtats.bts.gov/DL_SelectFields.asp?gnoyr_VQ={code}&QO_fu146_anzr=b0-gvzr"
_POST_PAGE = "https://www.transtats.bts.gov/DL_SelectFields.aspx?gnoyr_VQ={code}&QO_fu146_anzr=b0-gvzr"
_PREZIP = "https://transtats.bts.gov/PREZIP/{fname}"

_TIMEOUT = (15.0, 300.0)  # (connect, read) — large zips take a while


@transient_retry()
def _get(url: str, **kwargs) -> httpx.Response:
    resp = get(url, timeout=_TIMEOUT, **kwargs)
    resp.raise_for_status()
    return resp


@transient_retry()
def _post(url: str, data: dict, **kwargs) -> httpx.Response:
    # follow_redirects=False: the prezip postback signals the target file via a
    # 302 Location we read directly, so a 3xx is a success here — only raise on
    # genuine 4xx/5xx (transient ones are retried by the predicate).
    resp = post(url, data=data, timeout=_TIMEOUT, follow_redirects=False, **kwargs)
    if resp.status_code >= 400:
        resp.raise_for_status()
    return resp


def _parse_viewstate(html: str) -> dict:
    out = {}
    for name in ("__VIEWSTATE", "__VIEWSTATEGENERATOR", "__EVENTVALIDATION"):
        m = re.search(r'name="' + name + r'"[^>]*value="([^"]*)"', html)
        out[name] = htmlmod.unescape(m.group(1)) if m else ""
    return out


def _page_meta(code: str) -> dict:
    """GET the table's DL_SelectFields page and parse the period structure,
    available years, geography presence and the ASP.NET postback tokens."""
    html = _get(_GET_PAGE.format(code=code)).text

    year_block = re.search(r'<select name="cboYear".*?</select>', html, re.S)
    years = sorted(int(y) for y in re.findall(r'<option value="(\d+)"', year_block.group(0))) if year_block else []

    period_block = re.search(r'<select name="cboPeriod".*?</select>', html, re.S)
    periods = re.findall(r'<option value="(\d+)"', period_block.group(0)) if period_block else []
    periods = sorted(periods, key=int)

    if len(periods) == 12:
        period_type = "M"
    elif len(periods) == 4:
        period_type = "Q"
    else:
        period_type = "A"  # annual: one file per year, no period selector

    return {
        "years": years,
        "periods": periods,
        "period_type": period_type,
        "has_geo": "cboGeography" in html,
        "vs": _parse_viewstate(html),
        "has_period_select": period_block is not None,
    }


def _ordered_periods(meta: dict) -> list[tuple[int, str | None]]:
    """Stable (year, period_value) list ascending — history never reorders, new
    periods only append, so a count-based watermark stays valid across runs."""
    out: list[tuple[int, str | None]] = []
    for year in meta["years"]:
        if meta["period_type"] == "A":
            out.append((year, None))
        else:
            for per in meta["periods"]:
                out.append((year, per))
    return out


def _obs_fields(meta: dict, year: int, per: str | None) -> tuple[str, int, int | None]:
    """Derive a uniform observation date/year/period from the period coordinate."""
    if meta["period_type"] == "M":
        month = int(per)
        return f"{year}-{month:02d}-01", year, month
    if meta["period_type"] == "Q":
        q = int(per)
        return f"{year}-{(q - 1) * 3 + 1:02d}-01", year, q
    return f"{year}-01-01", year, None


def _batch_key(meta: dict, year: int, per: str | None) -> str:
    if meta["period_type"] == "M":
        return f"{year}-{int(per):02d}"
    if meta["period_type"] == "Q":
        return f"{year}-Q{int(per)}"
    return f"{year}"


def _discover_prezip_prefix(code: str, meta: dict) -> str:
    """Issue the prezip postback and read the redirect target to learn the
    table's stable /PREZIP/ filename prefix (e.g.
    'On_Time_Reporting_Carrier_On_Time_Performance_1987_present')."""
    data = dict(meta["vs"])
    data["cboYear"] = str(meta["years"][0])
    data["cboPeriod"] = meta["periods"][0] if meta["periods"] else "1"
    data["chkDownloadZip"] = "on"
    data["btnDownload"] = "Download"
    if meta["has_geo"]:
        data["cboGeography"] = "All"
    resp = _post(_POST_PAGE.format(code=code), data)
    loc = resp.headers.get("location", "")
    if "/PREZIP/" not in loc:
        raise RuntimeError(f"{code}: expected prezip redirect, got status={resp.status_code} loc={loc!r}")
    fname = loc.rsplit("/", 1)[1]
    prefix = re.sub(r"_\d+_\d+\.zip$", "", fname)
    if not prefix:
        raise RuntimeError(f"{code}: could not parse prezip prefix from {fname!r}")
    return prefix


def _download_prezip(prefix: str, year: int, per: str) -> bytes | None:
    """Direct GET of a constructed /PREZIP/ url. Returns None if the period file
    does not exist yet (404) — trailing future periods are expected to be absent."""
    fname = f"{prefix}_{year}_{per}.zip"
    try:
        resp = _get(_PREZIP.format(fname=fname))
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 404:
            print(f"  [skip] prezip not found: {fname}")
            return None
        raise
    return resp.content


def _download_custom(code: str, meta: dict, year: int, per: str | None) -> bytes | None:
    """POST the custom-download form (all variables) for one period. Returns the
    zip bytes, or None if the server reports no data / refuses the period."""
    for attempt in range(2):
        data = dict(meta["vs"])
        data["cboYear"] = str(year)
        data["chkAllVars"] = "on"
        data["btnDownload"] = "Download"
        if meta["has_geo"]:
            data["cboGeography"] = "All"
        if meta["has_period_select"] and per is not None:
            data["cboPeriod"] = per
        resp = _post(_POST_PAGE.format(code=code), data)
        ctype = resp.headers.get("content-type", "")
        if ctype.startswith("application/zip"):
            return resp.content
        # Not a zip: usually a stale viewstate ("not selected any variables")
        # or a no-data reload. Refresh tokens once, then give up on this period.
        if attempt == 0:
            print(f"  [retry] {code} {year}/{per}: non-zip response ({ctype}), refreshing viewstate")
            meta["vs"] = _parse_viewstate(_get(_GET_PAGE.format(code=code)).text)
            continue
        print(f"  [skip] {code} {year}/{per}: no data (content-type={ctype})")
        return None
    return None


def _data_member(zf: zipfile.ZipFile) -> str | None:
    """Pick the single data CSV from a download zip, ignoring the optional
    Term.csv / Documentation.csv glossary members."""
    candidates = [
        n for n in zf.namelist()
        if n.lower().endswith(".csv") and n.lower() not in ("term.csv", "documentation.csv")
    ]
    if not candidates:
        return None
    # The data CSV is by far the largest member.
    return max(candidates, key=lambda n: zf.getinfo(n).file_size)


def _write_batch(asset: str, content: bytes, obs_date: str, obs_year: int, obs_period: int | None) -> int:
    """Stream the data CSV out of the zip into an NDJSON batch, stamping each row
    with the injected observation fields. Returns the row count written (0 means
    nothing was written and no file was created)."""
    zf = zipfile.ZipFile(io.BytesIO(content))
    member = _data_member(zf)
    if member is None:
        print(f"  [skip] {asset}: no data CSV in zip ({zf.namelist()})")
        return 0
    with zf.open(member) as raw:
        reader = csv.reader(io.TextIOWrapper(raw, encoding="utf-8", errors="replace"))
        header = next(reader, None)
        if not header:
            return 0
        first = next(reader, None)
        if first is None:
            return 0
        n = 0
        with raw_writer(asset, "ndjson.gz", mode="wt", compression="gzip") as f:
            for rowvals in _chain_rows(first, reader):
                row = dict(zip(header, rowvals))
                row["obs_date"] = obs_date
                row["obs_year"] = obs_year
                row["obs_period"] = obs_period
                f.write(json.dumps(row, separators=(",", ":")))
                f.write("\n")
                n += 1
    return n


def _chain_rows(first, reader):
    yield first
    yield from reader


def fetch_one(node_id: str) -> None:
    """Firehose over one table's periods. Resumable via a per-table watermark."""
    code = node_id[len("bts-"):].upper().replace("-", "_")

    state = load_state(node_id)
    if state.get("schema_version") != STATE_VERSION:
        state = {}
    n_done = state.get("n_done", 0)

    meta = _page_meta(code)
    if not meta["years"]:
        raise RuntimeError(f"{code}: no years parsed from DL_SelectFields page")

    prefix = None
    if code in PREZIP_TABLES:
        prefix = _discover_prezip_prefix(code, meta)
        print(f"  {code}: prezip prefix = {prefix}")

    ordered = _ordered_periods(meta)
    start = max(0, n_done - OVERLAP_PERIODS)
    print(f"  {code}: {len(ordered)} periods, resuming at index {start} (n_done={n_done})")

    for i in range(start, len(ordered)):
        year, per = ordered[i]
        batch_key = _batch_key(meta, year, per)
        asset = f"{node_id}-{batch_key}"
        obs_date, obs_year, obs_period = _obs_fields(meta, year, per)

        if prefix is not None:
            content = _download_prezip(prefix, year, per)
        else:
            content = _download_custom(code, meta, year, per)

        if content is None:
            # Period genuinely unavailable (404 / no data). Do not advance the
            # watermark past it so it is retried on the next run once published.
            continue

        rows = _write_batch(asset, content, obs_date, obs_year, obs_period)
        if rows == 0:
            continue

        n_done = max(n_done, i + 1)
        save_state(node_id, {
            "schema_version": STATE_VERSION,
            "n_done": n_done,
            "last_batch": batch_key,
        })
        print(f"  {code} {batch_key}: {rows:,} rows -> {asset}")


DOWNLOAD_SPECS = [
    NodeSpec(
        id=f"bts-{eid.lower().replace('_', '-')}",
        fn=fetch_one,
        kind="download",
    )
    for eid in ENTITY_IDS
]


# One published Delta table per table-subset. Thin parse pass: surface the
# uniform injected observation date as a typed `date`, keep every source column
# (string-valued, lossless) plus the typed obs_year / obs_period.
TRANSFORM_SPECS = [
    SqlNodeSpec(
        id=f"{s.id}-transform",
        deps=[s.id],
        sql=(
            f'SELECT CAST(obs_date AS DATE) AS date, * EXCLUDE (obs_date) '
            f'FROM "{s.id}" '
            f'WHERE obs_date IS NOT NULL'
        ),
    )
    for s in DOWNLOAD_SPECS
]
