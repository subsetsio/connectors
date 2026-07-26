"""Central Bureau of Statistics (Israel) — connector node module.

Two source APIs (no auth, a browser User-Agent is set by subsets_utils.get):

* Time Series DataBank — ``apis.cbs.gov.il/series``. The comprehensive national
  corpus. ``/catalog/level?id=1`` lists the 33 top-level subjects; ``/data/path?id=<code>``
  returns the ENTIRE subtree under a path code in one response (pagination on this
  endpoint is non-functional — pagesize/Page are ignored, the full set always comes
  back), each series record carrying full metadata (id, unit, time/frequency, the
  5-level subject path, last-update date) plus an ``obs`` array of {TimePeriod, Value}.
  We crawl one call per subject. ``series-catalog`` projects the per-series metadata
  (light, last=1); ``series-values`` keeps every observation, written one parquet
  batch per subject (the corpus is millions of rows).

* Price Indices — ``api.cbs.gov.il/index`` (note the SINGULAR host). ``/catalog/catalog``
  lists 13 index chapters; ``/data/price_all?chapter=<id>`` is a per-chapter bulk XML
  dump that enumerates every index series (code + name) but only at its LATEST period
  (the many <index_base> elements are alternative rebasings of that latest value, not
  history). For history we then hit ``/data/price?id=<code>`` per code, which returns the
  full monthly series (paged 100 observations/page; large pagesize 500s, so we follow the
  page count) with numeric month and the current-base level under ``currBase``.

Stateless full re-pull every run (revisions picked up for free); freshness is the
maintain step's concern. series-values is written as per-subject batches purely for
memory — not for resumption; a supervisor interrupt simply restarts the crawl.
"""

import xml.etree.ElementTree as ET
from datetime import datetime, timezone

import pyarrow as pa
from subsets_utils import (
    NodeSpec,
    get,
    save_raw_parquet,
)

SERIES_BASE = "https://apis.cbs.gov.il/series"
INDEX_BASE = "https://api.cbs.gov.il/index"

SLUG = "central-bureau-of-statistics"

# ---------------------------------------------------------------- HTTP helpers


def _get_json(url, **params):
    resp = get(url, params=params, timeout=(10.0, 420.0))
    resp.raise_for_status()
    return resp.json()


def _get_text(url, **params):
    resp = get(url, params=params, timeout=(10.0, 420.0))
    resp.raise_for_status()
    return resp.text


def _subject_codes():
    """The 33 top-level subject path codes (level-1 of the catalog hierarchy)."""
    j = _get_json(f"{SERIES_BASE}/catalog/level", id=1, lang="en", format="json")
    cats = j.get("catalogs", {}).get("catalog", [])
    codes = [c["path"][0] for c in cats if c.get("path")]
    if len(codes) < 20:
        raise AssertionError(f"only {len(codes)} subjects discovered; catalog/level likely broke")
    return codes


def _chapter_ids():
    """Distinct price-index chapter ids (params for /data/price_all)."""
    j = _get_json(f"{INDEX_BASE}/catalog/catalog", lang="en", format="json")
    chapters = j.get("chapters", [])
    ids = []
    for c in chapters:
        cid = c.get("chapterId")
        if cid and cid not in ids:
            ids.append(cid)
    if not ids:
        raise AssertionError("no price-index chapters discovered")
    return ids


def _series_meta(s):
    path = s.get("path") or {}

    def nm(key):
        return (path.get(key) or {}).get("name")

    def val(key):
        return (path.get(key) or {}).get("value")

    return {
        "series_id": s.get("id"),
        "subject_code": val("level1"),
        "level1_name": nm("level1"),
        "level2_name": nm("level2"),
        "level3_name": nm("level3"),
        "level4_name": nm("level4"),
        "name_id": val("name_id"),
        "series_name": nm("name_id"),
        "unit_name": (s.get("unit") or {}).get("name"),
        "frequency": (s.get("time") or {}).get("name"),
        "data_type": (s.get("data") or {}).get("name"),
        "price_basis": (s.get("price") or {}).get("name"),
        "calc": (s.get("calc") or {}).get("name"),
        "last_update": s.get("update"),
    }


def _subject_taxonomy_rows():
    """Derive the hierarchy from series path metadata.

    Direct /catalog/level child calls are brittle (CBS returns HTTP 500 for
    several level/subject combinations), while /data/path for each top-level
    subject embeds every level's id/name in each series record.
    """
    seen = {}
    for code in _subject_codes():
        j = _get_json(f"{SERIES_BASE}/data/path", id=code, last=1, format="json", lang="en")
        for s in j.get("DataSet", {}).get("Series", []):
            path = s.get("path") or {}
            path_parts = []
            for level in range(1, 5):
                item = path.get(f"level{level}") or {}
                value = item.get("value")
                name = item.get("name")
                if value is None or name is None:
                    continue
                path_parts.append(str(value))
                key = tuple(path_parts)
                if key not in seen:
                    seen[key] = {
                        "level": level,
                        "subject_code": _to_int(value),
                        "subject_name": name,
                        "path": "/".join(path_parts),
                        "parent_path": "/".join(path_parts[:-1]) or None,
                    }
    rows = sorted(seen.values(), key=lambda r: (r["level"], r["path"]))
    if len(rows) < 100:
        raise AssertionError(f"only {len(rows)} subject taxonomy rows discovered")
    return rows


# ---------------------------------------------------------------- series catalog

CATALOG_SCHEMA = pa.schema([
    ("series_id", pa.int64()),
    ("subject_code", pa.int64()),
    ("level1_name", pa.string()),
    ("level2_name", pa.string()),
    ("level3_name", pa.string()),
    ("level4_name", pa.string()),
    ("name_id", pa.int64()),
    ("series_name", pa.string()),
    ("unit_name", pa.string()),
    ("frequency", pa.string()),
    ("data_type", pa.string()),
    ("price_basis", pa.string()),
    ("calc", pa.string()),
    ("last_update", pa.string()),
])


def fetch_series_catalog(node_id: str) -> None:
    """Reference catalog: one row per CBS time series with its metadata.

    Accumulated across all subjects into a single parquet (metadata is small even
    at tens of thousands of series)."""
    asset = node_id
    rows = []
    for code in _subject_codes():
        j = _get_json(f"{SERIES_BASE}/data/path", id=code, last=1, format="json", lang="en")
        for s in j.get("DataSet", {}).get("Series", []):
            rows.append(_series_meta(s))
    if not rows:
        raise AssertionError("series catalog crawl produced 0 rows")
    table = pa.Table.from_pylist(rows, schema=CATALOG_SCHEMA)
    save_raw_parquet(table, asset)


# ---------------------------------------------------------------- series values

VALUES_SCHEMA = pa.schema([
    ("series_id", pa.int64()),
    ("frequency", pa.string()),
    ("period", pa.string()),
    ("value", pa.float64()),
])


def fetch_series_values(node_id: str) -> None:
    """Long-format observations across every CBS time series, one parquet batch
    per subject (batch_key = subject code). The transform's dep view glob-unions
    all batches automatically."""
    for code in _subject_codes():
        j = _get_json(f"{SERIES_BASE}/data/path", id=code, format="json", lang="en")
        rows = []
        for s in j.get("DataSet", {}).get("Series", []):
            sid = s.get("id")
            freq = (s.get("time") or {}).get("name")
            for ob in s.get("obs") or []:
                rows.append({
                    "series_id": sid,
                    "frequency": freq,
                    "period": ob.get("TimePeriod"),
                    "value": ob.get("Value"),
                })
        if not rows:
            continue
        table = pa.Table.from_pylist(rows, schema=VALUES_SCHEMA)
        save_raw_parquet(table, f"{node_id}-{code}")


# ---------------------------------------------------------------- price parsing


def _enumerate_price_codes():
    """Walk every chapter's /data/price_all snapshot and return a de-duplicated list
    of (chapter_id, chapter_name, code, index_name). This enumerates the full set of
    index series — the snapshot lists each series once at its latest period."""
    out = []
    seen = set()
    for cid in _chapter_ids():
        xml_text = _get_text(f"{INDEX_BASE}/data/price_all", lang="en", chapter=cid, download="false")
        root = ET.fromstring(xml_text)
        for chapter in root.findall("chapter"):
            chapter_name = chapter.get("name")
            for month in chapter.findall("month"):
                for idx in month.findall("index"):
                    code = idx.get("code")
                    index_name = idx.findtext("index_name")
                    key = (cid, code)
                    if code is None or key in seen:
                        continue
                    seen.add(key)
                    out.append((cid, chapter_name, code, index_name))
    if not out:
        raise AssertionError("price-index enumeration produced 0 codes")
    return out


def _fetch_price_history(code):
    """Full monthly history for one index code via /data/price, following the page
    count (100 obs/page). Returns a list of date-record dicts as the API delivers them."""
    end_year = datetime.now(tz=timezone.utc).year + 1
    return _fetch_price_history_range(code, 1948, end_year, allow_window_fallback=True)


def _fetch_price_history_range(code, start_year, end_year, *, allow_window_fallback=False):
    """Fetch one price-index code for an inclusive year range.

    Some valid CBS price series report multiple pages but return HTTP 500 for
    page > 1. When that happens on the full-history call, refetch in small
    windows whose monthly observations fit on the first page.
    """
    recs = []
    page = 1
    max_pages = 1000  # safety ceiling; raises rather than truncating silently
    while True:
        try:
            j = _get_json(
                f"{INDEX_BASE}/data/price", id=code, startPeriod=f"01-{start_year}",
                endPeriod=f"12-{end_year}", format="json", lang="en", Page=page,
            )
        except Exception:
            if allow_window_fallback:
                fetched_years = [_to_int(d.get("year")) for d in recs]
                fetched_years = [y for y in fetched_years if y is not None]
                oldest_year = min(fetched_years, default=end_year + 1)
                return _fetch_price_history_windowed(
                    code, start_year, oldest_year, existing=recs
                ) + recs
            raise
        months = j.get("month") or []
        for entry in months:
            for d in entry.get("date") or []:
                recs.append(d)
        paging = j.get("paging") or {}
        total_items = paging.get("total_items")
        if total_items is not None and len(recs) >= int(total_items):
            break
        last_page = paging.get("last_page") or 1
        if page >= last_page:
            break
        page += 1
        if page > max_pages:
            raise AssertionError(f"price code {code}: exceeded {max_pages} pages")
    return recs


def _fetch_price_history_windowed(code, start_year, end_year, *, existing=()):
    rows = []
    seen = {(d.get("year"), d.get("month")) for d in existing}
    for year in range(start_year, end_year + 1):
        try:
            batch = _fetch_price_history_range(code, year, year)
        except Exception:
            # CBS returns {"Message":"Error: Price Data"} for some historical
            # annual slices of otherwise valid series. Preserve the rest of the
            # series instead of failing the whole price-index corpus.
            continue
        for d in batch:
            key = (d.get("year"), d.get("month"))
            if key in seen:
                continue
            seen.add(key)
            rows.append(d)
    return rows


def _to_int(x):
    try:
        return int(x)
    except (TypeError, ValueError):
        return None


def _to_float(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return None


# ---------------------------------------------------------------- price catalog

PRICE_CATALOG_SCHEMA = pa.schema([
    ("chapter_id", pa.string()),
    ("chapter_name", pa.string()),
    ("code", pa.int64()),
    ("index_name", pa.string()),
])


def fetch_price_index_catalog(node_id: str) -> None:
    """Reference catalog of price-index series: distinct (chapter, code, name)."""
    asset = node_id
    rows = [
        {"chapter_id": cid, "chapter_name": chapter_name, "code": _to_int(code), "index_name": index_name}
        for (cid, chapter_name, code, index_name) in _enumerate_price_codes()
    ]
    if not rows:
        raise AssertionError("price-index catalog crawl produced 0 rows")
    table = pa.Table.from_pylist(rows, schema=PRICE_CATALOG_SCHEMA)
    save_raw_parquet(table, asset)


# ---------------------------------------------------------------- price values

PRICE_VALUES_SCHEMA = pa.schema([
    ("code", pa.int64()),
    ("index_name", pa.string()),
    ("chapter_id", pa.string()),
    ("chapter_name", pa.string()),
    ("year", pa.int64()),
    ("month", pa.int64()),
    ("percent", pa.float64()),
    ("percent_year", pa.float64()),
    ("base_desc", pa.string()),
    ("value", pa.float64()),
])


def fetch_price_index_values(node_id: str) -> None:
    """Long-format monthly price-index history across all chapters. One parquet batch
    per chapter (batch_key = chapter id); within a chapter, full history is fetched per
    code from /data/price (value = current-base index level)."""
    # Group enumerated codes by chapter so each batch is one chapter's worth.
    by_chapter = {}
    for (cid, chapter_name, code, index_name) in _enumerate_price_codes():
        by_chapter.setdefault(cid, (chapter_name, []))[1].append((code, index_name))

    for cid, (chapter_name, codes) in by_chapter.items():
        rows = []
        for code, index_name in codes:
            for d in _fetch_price_history(code):
                cur = d.get("currBase") or {}
                rows.append({
                    "code": _to_int(code),
                    "index_name": index_name,
                    "chapter_id": cid,
                    "chapter_name": chapter_name,
                    "year": _to_int(d.get("year")),
                    "month": _to_int(d.get("month")),
                    "percent": _to_float(d.get("percent")),
                    "percent_year": _to_float(d.get("percentYear")),
                    "base_desc": cur.get("baseDesc"),
                    "value": _to_float(cur.get("value")),
                })
        if not rows:
            continue
        table = pa.Table.from_pylist(rows, schema=PRICE_VALUES_SCHEMA)
        save_raw_parquet(table, f"{node_id}-{cid}")


# ---------------------------------------------------------------- subjects

SUBJECTS_SCHEMA = pa.schema([
    ("level", pa.int64()),
    ("subject_code", pa.int64()),
    ("subject_name", pa.string()),
    ("path", pa.string()),
    ("parent_path", pa.string()),
])


def fetch_subjects(node_id: str) -> None:
    """Reference taxonomy for CBS time-series subjects, one row per path node."""
    table = pa.Table.from_pylist(_subject_taxonomy_rows(), schema=SUBJECTS_SCHEMA)
    save_raw_parquet(table, node_id)


# ---------------------------------------------------------------- specs

DOWNLOAD_SPECS = [
    NodeSpec(id=f"{SLUG}-series-catalog", fn=fetch_series_catalog, kind="download"),
    NodeSpec(id=f"{SLUG}-series-values", fn=fetch_series_values, kind="download"),
    NodeSpec(id=f"{SLUG}-price-index-catalog", fn=fetch_price_index_catalog, kind="download"),
    NodeSpec(id=f"{SLUG}-price-index-values", fn=fetch_price_index_values, kind="download"),
    NodeSpec(id=f"{SLUG}-subjects", fn=fetch_subjects, kind="download"),
]
