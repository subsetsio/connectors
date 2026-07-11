"""KFF State Health Facts connector.

Each State Health Facts indicator publishes one Delta table. The data lives in a
purpose-built, server-rendered block on every indicator page:

    <article class="kff-interactive-llm-data" aria-hidden="true">
      <h2>{indicator title}</h2>
      <main>
        <figure><h3>{timeframe}</h3><table><thead>...<tbody>...</table></figure>
        ... one figure per timeframe (year) ...
        <figure><h3>Notes</h3>...</figure>     (skipped — not data)
      </main>
    </article>

Each data figure is one timeframe; its table has a `Location` column plus one or
more indicator-specific metric columns (some indicators repeat the metric set for
multiple data views, e.g. percent then number — disambiguated here by col_index).
We normalize every page to one fixed LONG schema:
(location, timeframe, col_index, metric, value_raw, value) — uniform across all
836 indicators, so one schema and one thin transform per subset.

Fetch shape: stateless full re-pull. Each page is a single GET that returns the
entire indicator (all locations x all timeframes x all columns); the corpus is
~836 small pages with no incremental filter on the page itself, so we re-fetch
the whole table every run and overwrite. The generic URL
https://www.kff.org/state-health-policy-data/state-indicator/<slug>/ 301-redirects
to the indicator's canonical category path (redirects are followed), so the slug
alone identifies the page — no per-entity URL map needed.
"""

import html as _html
import re

import pyarrow as pa

from subsets_utils import (
    NodeSpec,
    get,
    save_raw_parquet,
)

# --- entity union (indicator slugs + reference taxonomy) -----------------
from constants import ENTITY_IDS

_URL = "https://www.kff.org/state-health-policy-data/state-indicator/{slug}/"

SCHEMA = pa.schema([
    ("location", pa.string()),
    ("timeframe", pa.string()),
    ("col_index", pa.int32()),
    ("metric", pa.string()),
    ("value_raw", pa.string()),
    ("value", pa.float64()),
])

CATEGORY_SCHEMA = pa.schema([
    ("id", pa.int64()),
    ("name", pa.string()),
    ("slug", pa.string()),
    ("parent", pa.int64()),
    ("count", pa.int64()),
])

# figure h3 labels that are documentation, not data tables
_META_FIGURES = {"notes", "sources", "definitions", "methodology"}
# cell tokens that mean "no value"
_NULL_TOKENS = {
    "", "n/a", "na", "nr", "nsd", "n.a.", "n/r", "*", "--", "-", "—",
    "–", "suppressed", "not available", "not reported", ".",
}


def _fetch_html(url: str) -> str:
    resp = get(url, timeout=(10.0, 120.0))
    resp.raise_for_status()
    return resp.text


def _fetch_json(url: str):
    resp = get(url, timeout=(10.0, 120.0))
    resp.raise_for_status()
    return resp.json()


def _clean_value(raw: str):
    """Return a float for the cell, or None if it isn't a number."""
    t = raw.strip()
    low = t.lower()
    if low in _NULL_TOKENS:
        return None
    pct = t.endswith("%")
    s = t.replace("$", "").replace(",", "").replace("%", "")
    s = s.replace("<", "").replace(">", "").strip()
    if not s or s.lower() in _NULL_TOKENS:
        return None
    try:
        v = float(s)
    except ValueError:
        return None
    return v / 100.0 if pct else v


def _strip_tags(s: str) -> str:
    return _html.unescape(re.sub(r"<[^>]+>", "", s)).strip()


def _parse_rows(html_text: str):
    """Parse the kff-interactive-llm-data block into long-format dict rows."""
    art = re.search(
        r'<article class="kff-interactive-llm-data"[\s\S]*?</article>',
        html_text,
    )
    if not art:
        return []
    block = art.group(0)

    rows = []
    for fig in re.findall(r"<figure>([\s\S]*?)</figure>", block):
        h3 = re.search(r"<h3>([\s\S]*?)</h3>", fig)
        if not h3:
            continue
        timeframe = _strip_tags(h3.group(1))
        if timeframe.lower() in _META_FIGURES:
            continue

        thead = re.search(r"<thead>([\s\S]*?)</thead>", fig)
        tbody = re.search(r"<tbody>([\s\S]*?)</tbody>", fig)
        if not thead or not tbody:
            continue
        headers = [_strip_tags(h) for h in re.findall(r"<th>([\s\S]*?)</th>", thead.group(1))]
        # a data table starts with a Location column
        if not headers or headers[0].lower() != "location":
            continue

        for tr in re.findall(r"<tr>([\s\S]*?)</tr>", tbody.group(1)):
            cells = [_strip_tags(c) for c in re.findall(r"<td>([\s\S]*?)</td>", tr)]
            if not cells:
                continue
            location = cells[0]
            for idx in range(1, len(cells)):
                metric = headers[idx] if idx < len(headers) else f"col_{idx}"
                raw = cells[idx]
                rows.append({
                    "location": location,
                    "timeframe": timeframe,
                    "col_index": idx,
                    "metric": metric,
                    "value_raw": raw,
                    "value": _clean_value(raw),
                })
    return rows


def fetch_one(node_id: str) -> None:
    asset = node_id  # the spec id IS the asset name
    slug = node_id[len("kff-"):]
    if slug == "state-categories":
        rows = []
        page = 1
        while True:
            url = (
                "https://www.kff.org/wp-json/wp/v2/state-category"
                f"?per_page=100&page={page}&_fields=id,name,slug,parent,count"
            )
            batch = _fetch_json(url)
            if not batch:
                break
            for item in batch:
                rows.append({
                    "id": item["id"],
                    "name": _html.unescape(item.get("name") or "").strip(),
                    "slug": item.get("slug"),
                    "parent": item.get("parent"),
                    "count": item.get("count"),
                })
            if len(batch) < 100:
                break
            page += 1
        if not rows:
            raise ValueError(f"{asset}: no category terms fetched")
        save_raw_parquet(pa.Table.from_pylist(rows, schema=CATEGORY_SCHEMA), asset)
        return

    url = _URL.format(slug=slug)
    html_text = _fetch_html(url)
    rows = _parse_rows(html_text)
    if not rows:
        # No parseable data table on the page — a real, permanent problem for
        # this indicator (format change or non-tabular page). Fail loudly so the
        # run surfaces it rather than publishing an empty table.
        raise ValueError(f"{asset}: no data rows parsed from {url}")
    table = pa.Table.from_pylist(rows, schema=SCHEMA)
    save_raw_parquet(table, asset)


DOWNLOAD_SPECS = [
    NodeSpec(
        id=f"kff-{eid.lower().replace('_', '-')}",
        fn=fetch_one,
        kind="download",
    )
    for eid in ENTITY_IDS
]
