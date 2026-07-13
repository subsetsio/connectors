"""BTS (Bureau of Transportation Statistics) — TranStats connector.

One download spec per TranStats data table (the accept-decided entity union).
Every table is fetched from the TranStats "custom download" surface at
``www.transtats.bts.gov/DL_SelectFields`` — an ASP.NET form. The table's shape
is discovered at runtime from that page (never hardcoded), and the fetch adapts
to one of three shapes:

* **prezip time-series** (the high-volume aviation tables — On-Time Performance,
  DB1B Market/Ticket/Coupon): the download button 302-redirects to a stable
  ``/PREZIP/<prefix>_<year>_<period>.zip`` file. We discover the prefix once from
  that redirect, then GET the pre-zipped period files directly (fast, static
  host). One CSV per period.
* **custom time-series** (every other periodic table): an ASP.NET form POST with
  ``chkAllVars`` selected returns a zip containing one data CSV for the requested
  year/period.
* **static lookup** (reference tables whose year/period selectors offer only
  "Not Applicable" — e.g. Master Coordinate): a single form POST with
  ``cboYear=All`` yields one CSV; there is no time dimension.

Time-series tables are a **firehose** over their periods: each period is written
as its own NDJSON batch (``bts-<code>-<batch_key>``) and a per-table watermark
(count of periods ingested) is saved after every batch, so a supervisor
interrupt resumes cleanly. A small overlap re-fetches the most recent periods
each run to absorb source revisions. Lookup tables write a single ``-all`` batch.

Raw is written as **NDJSON with string cell values** — lossless (no code/type
corruption) and drift-safe: column sets change across decades for some tables,
and ``read_json_auto`` unions batch files by name. Time-series rows are stamped
with an injected ``obs_date`` / ``obs_year`` / ``obs_period`` derived from the
period being fetched, giving every published subset a uniform typed time
dimension regardless of which time columns the source CSV happens to carry.

The full corpus is large (decades of monthly flight-level data); there is no
``since``/cursor filter on the source, so partitioning *is* the incremental unit
and the firehose drains forward across supervisor-bounded runs.
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
    configure_http,
    get,
    post,
    load_state,
    save_state,
    raw_writer,
    transient_retry,
)

from constants import ENTITY_IDS

# Bumped when the state/batch contract changes (v2: lookup handling + no
# obs stamping for lookup tables).
STATE_VERSION = 2

# Re-fetch this many of the most recently ingested periods each run to absorb
# source revisions (BTS revises recent months/quarters). Duplicates are dropped
# downstream; this is the safety, not a bug.
OVERLAP_PERIODS = 2

# The TranStats IIS app serves a contentless page (no year selector) to the
# default library User-Agent when hit from a datacenter IP. A browser UA gets
# the real form. ASCII only (httpx/urllib3 reject non-ASCII header bytes).
_UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
       "(KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36")

_GET_PAGE = "https://www.transtats.bts.gov/DL_SelectFields.asp?gnoyr_VQ={code}&QO_fu146_anzr=b0-gvzr"
_POST_PAGE = "https://www.transtats.bts.gov/DL_SelectFields.aspx?gnoyr_VQ={code}&QO_fu146_anzr=b0-gvzr"
_PREZIP = "https://transtats.bts.gov/PREZIP/{fname}"

_TIMEOUT = (15.0, 600.0)  # (connect, read) — large zips take a while


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


def _select_options(html: str, name: str) -> list[str]:
    m = re.search(r'<select name="' + name + r'".*?</select>', html, re.S)
    if not m:
        return []
    return re.findall(r'<option[^>]*value="([^"]*)"', m.group(0))


def _probe_table(code: str) -> dict:
    """GET the table's DL_SelectFields page and parse its shape: numeric years +
    period structure (time-series) vs an "All"-only selector (static lookup),
    plus geography presence and the ASP.NET postback tokens."""
    html = _get(_GET_PAGE.format(code=code)).text

    yopts = _select_options(html, "cboYear")
    popts = _select_options(html, "cboPeriod")
    if not yopts:
        # No year selector at all: almost certainly a bot-block or maintenance
        # page rather than a real table. Surface enough to triage a CI failure
        # (the 2026-07 run failed here, opaquely, on every table).
        title = re.search(r"<title>(.*?)</title>", html, re.S)
        raise RuntimeError(
            f"{code}: DL_SelectFields page had no cboYear selector "
            f"(html_len={len(html)}, title={(title.group(1).strip()[:80] if title else 'n/a')!r}) "
            f"— likely a bot-block / maintenance page, not a real empty table"
        )

    years = sorted(int(y) for y in yopts if y.isdigit())
    period_num = sorted(int(p) for p in popts if p.isdigit())
    lookup = not years  # cboYear offers only "All" -> a static reference table

    if len(period_num) == 12:
        period_type = "M"
    elif period_num and set(period_num) <= {1, 2, 3, 4}:
        period_type = "Q"
    elif period_num:
        # A month-subset selector (e.g. quarter-end months 3/6/9/12). These are
        # month codes, not quarter numbers.
        period_type = "M"
    else:
        period_type = "A"  # annual: one file per year, no period selector

    return {
        "code": code,
        "lookup": lookup,
        "years": years,
        "period_type": period_type,
        "periods": [str(p) for p in period_num],
        "has_geo": "cboGeography" in html,
        "has_period_select": bool(popts) and bool(period_num),
        "vs": _parse_viewstate(html),
    }


def _detect_prezip_prefix(meta: dict) -> str | None:
    """One postback to learn whether the table exposes a /PREZIP/ surface and,
    if so, its stable filename prefix (e.g.
    'On_Time_Reporting_Carrier_On_Time_Performance_1987_present'). Returns None
    for tables that only serve the on-demand custom download."""
    if meta["lookup"] or not meta["has_period_select"]:
        return None
    data = dict(meta["vs"])
    data["cboYear"] = str(meta["years"][-1])
    data["cboPeriod"] = meta["periods"][0] if meta["periods"] else "1"
    data["chkDownloadZip"] = "on"
    data["btnDownload"] = "Download"
    if meta["has_geo"]:
        data["cboGeography"] = "All"
    resp = _post(_POST_PAGE.format(code=meta["code"]), data)
    loc = resp.headers.get("location", "")
    if resp.status_code in (301, 302) and "/PREZIP/" in loc:
        fname = loc.rsplit("/", 1)[1]
        prefix = re.sub(r"_\d+_\d+\.zip$", "", fname)
        return prefix or None
    return None


def _ordered_periods(meta: dict) -> list[tuple[int, str | None]]:
    """Stable (year, period_value) list ascending — history never reorders, new
    periods only append, so a count-based watermark stays valid across runs."""
    out: list[tuple[int, str | None]] = []
    for year in meta["years"]:
        if not meta["has_period_select"]:
            out.append((year, None))
        else:
            for per in meta["periods"]:
                out.append((year, per))
    return out


def _obs_fields(meta: dict, year: int, per: str | None) -> tuple[str, int, int | None]:
    """Derive a uniform observation date/year/period from the period coordinate."""
    if per is not None and meta["period_type"] == "M":
        month = int(per)
        return f"{year}-{month:02d}-01", year, month
    if per is not None and meta["period_type"] == "Q":
        q = int(per)
        return f"{year}-{(q - 1) * 3 + 1:02d}-01", year, q
    return f"{year}-01-01", year, None


def _batch_key(meta: dict, year: int, per: str | None) -> str:
    if per is not None and meta["period_type"] == "M":
        return f"{year}-{int(per):02d}"
    if per is not None and meta["period_type"] == "Q":
        return f"{year}-Q{int(per)}"
    return f"{year}"


def _download_prezip(prefix: str, year: int, per: str) -> bytes | None:
    """Direct GET of a constructed /PREZIP/ url. Returns None if the period file
    does not exist yet (404) — trailing future periods are expected to be
    absent, so the caller does not advance the watermark past them."""
    fname = f"{prefix}_{year}_{per}.zip"
    try:
        resp = _get(_PREZIP.format(fname=fname))
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 404:
            print(f"  [skip] prezip not found: {fname}")
            return None
        raise
    return resp.content


def _download_custom(meta: dict, year, per: str | None) -> bytes | None:
    """POST the custom-download form (all variables) for one period. `year` may
    be the literal 'All' for a static lookup table. Returns the zip bytes, or
    None if the server reports no data / refuses the period."""
    code = meta["code"]
    for attempt in range(2):
        data = dict(meta["vs"])
        data["cboYear"] = str(year)
        data["chkAllVars"] = "on"
        data["btnDownload"] = "Download"
        if meta["has_geo"]:
            data["cboGeography"] = "All"
        # Periodic tables send the specific period; annual and lookup tables
        # whose selector offers only "Not Applicable" send "All".
        if meta["has_period_select"] and per is not None:
            data["cboPeriod"] = str(per)
        else:
            data["cboPeriod"] = "All"
        resp = _post(_POST_PAGE.format(code=code), data)
        ctype = resp.headers.get("content-type", "").lower()
        if ctype.startswith("application/zip") or ctype.startswith("application/x-zip"):
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


def _chain_rows(first, reader):
    yield first
    yield from reader


def _write_batch(asset: str, content: bytes, obs_date, obs_year, obs_period, *, inject: bool) -> int:
    """Stream the data CSV out of the zip into an NDJSON batch. Time-series
    batches stamp each row with the injected observation fields; lookup batches
    (inject=False) are written as-is. Returns the row count written (0 means
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
                if inject:
                    row["obs_date"] = obs_date
                    row["obs_year"] = obs_year
                    row["obs_period"] = obs_period
                f.write(json.dumps(row, separators=(",", ":")))
                f.write("\n")
                n += 1
    return n


def fetch_one(node_id: str) -> None:
    """Fetch one TranStats table. Shape is discovered at runtime; time-series
    tables firehose over their periods (resumable via a per-table watermark),
    lookup tables write a single batch."""
    configure_http(headers={"User-Agent": _UA})
    code = node_id[len("bts-"):].upper().replace("-", "_")

    meta = _probe_table(code)

    if meta["lookup"]:
        content = _download_custom(meta, "All", None)
        if content is None:
            raise RuntimeError(f"{code}: static lookup download returned no zip")
        rows = _write_batch(f"{node_id}-all", content, None, None, None, inject=False)
        if rows == 0:
            raise RuntimeError(f"{code}: static lookup produced 0 rows")
        print(f"  {code} lookup: {rows:,} rows -> {node_id}-all")
        return

    if not meta["years"]:
        raise RuntimeError(f"{code}: no years parsed from DL_SelectFields page")

    state = load_state(node_id)
    if state.get("schema_version") != STATE_VERSION:
        state = {}
    n_done = state.get("n_done", 0)

    prefix = _detect_prezip_prefix(meta)
    if prefix:
        print(f"  {code}: prezip prefix = {prefix}")

    ordered = _ordered_periods(meta)
    start = max(0, n_done - OVERLAP_PERIODS)
    print(f"  {code}: {len(ordered)} periods, resuming at index {start} (n_done={n_done})")

    for i in range(start, len(ordered)):
        year, per = ordered[i]
        batch_key = _batch_key(meta, year, per)
        asset = f"{node_id}-{batch_key}"
        obs_date, obs_year, obs_period = _obs_fields(meta, year, per)

        if prefix is not None and per is not None:
            content = _download_prezip(prefix, year, per)
        else:
            content = _download_custom(meta, year, per)

        if content is None:
            # Period genuinely unavailable (404 / no data). Do not advance the
            # watermark past it so it is retried on the next run once published.
            continue

        rows = _write_batch(asset, content, obs_date, obs_year, obs_period, inject=True)
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
