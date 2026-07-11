"""Ofgem Data Portal connector.

Source: the Ofgem (GB energy regulator) Data Portal at
https://www.ofgem.gov.uk/data-portal/all-charts — ~188 interactive charts of
GB energy-market statistics (retail/wholesale prices, debt & arrears, market
shares, customer satisfaction, network performance, renewable-scheme uptake).

Mechanism (per research, chosen = ``everviz_inject``): every chart is rendered
by everviz (Highcharts' hosted SaaS). ``GET https://app.everviz.com/inject/
{token}/`` returns a JS inject script that embeds the full Highcharts options
object inline; the raw numbers live in ``options.data.csv`` — a CSV string
whose item delimiter is either ',' or ';' (both occur, detected per chart),
first column = the x-axis category (date/quarter/label), remaining columns =
named series. The everviz token for each chart comes from the data-portal
listing API and is pinned per chart in ``ENTITY_TOKENS`` below (built at
implement time from the collect catalog).

Fetch shape: stateless full re-pull. Each chart is a tiny table (<50KB) with no
incremental filter (research: "no incremental — full corpus per refresh"), so
every refresh re-fetches and overwrites. Each chart is normalised to a uniform
long format — (category, series, value) — and published as its own Delta table.
"""

import csv as _csv
import io
import json
import re


from subsets_utils import (
    NodeSpec,
    get,
    save_raw_ndjson,
    transient_retry,
)
from constants import ENTITY_TOKENS, ENTITY_IDS

INJECT_URL = "https://app.everviz.com/inject/{token}/"


@transient_retry()
def _fetch_inject(token: str) -> str:
    resp = get(INJECT_URL.format(token=token), timeout=(10.0, 120.0))
    resp.raise_for_status()
    return resp.text


def _balanced_object(s: str, start: int) -> str | None:
    """Return the brace-balanced ``{...}`` substring beginning at ``start``,
    respecting JSON string quoting/escapes."""
    depth = 0
    in_str = False
    esc = False
    for j in range(start, len(s)):
        c = s[j]
        if in_str:
            if esc:
                esc = False
            elif c == "\\":
                esc = True
            elif c == '"':
                in_str = False
        else:
            if c == '"':
                in_str = True
            elif c == "{":
                depth += 1
            elif c == "}":
                depth -= 1
                if depth == 0:
                    return s[start : j + 1]
    return None


def _extract_options(js: str) -> dict:
    """Extract the inline Highcharts options object from an everviz inject
    script. The script assigns ``options = { ... }``; we slice that object out
    and JSON-parse it."""
    m = re.search(r"options\s*=\s*", js)
    if not m:
        raise ValueError("everviz inject: no `options =` assignment found")
    brace = js.find("{", m.end() - 1)
    if brace < 0:
        raise ValueError("everviz inject: options assignment has no object")
    obj = _balanced_object(js, brace)
    if obj is None:
        raise ValueError("everviz inject: unbalanced options object")
    return json.loads(obj)


def _detect_delimiter(header_line: str) -> str:
    best, best_n = ",", 0
    for d in (",", ";"):
        n = len(next(_csv.reader([header_line], delimiter=d)))
        if n > best_n:
            best, best_n = d, n
    return best


def _parse_value(cell: str):
    cell = (cell or "").strip()
    if cell in ("", "-", "n/a", "N/A", "NA", "null", "None"):
        return None
    try:
        return float(cell)
    except ValueError:
        return None


def _csv_to_long(csv_text: str) -> list[dict]:
    """Normalise a Highcharts ``data.csv`` blob to long format: one row per
    (category, series) cell. Column 0 is the x-axis category; every other
    column is a named numeric series."""
    text = csv_text.replace("\r\n", "\n").replace("\r", "\n")
    first_nl = text.find("\n")
    header_line = text if first_nl < 0 else text[:first_nl]
    delim = _detect_delimiter(header_line)
    reader = list(_csv.reader(io.StringIO(text), delimiter=delim))
    if not reader:
        return []
    header = reader[0]
    series_names = [(h.strip() or f"series_{i}") for i, h in enumerate(header)]
    rows: list[dict] = []
    for rec in reader[1:]:
        if not rec or not any(c.strip() for c in rec):
            continue
        category = (rec[0] or "").strip()
        for i in range(1, len(rec)):
            if i >= len(series_names):
                break
            value = _parse_value(rec[i])
            rows.append(
                {
                    "category": category,
                    "series": series_names[i],
                    "value": value,
                }
            )
    return rows


def fetch_one(node_id: str) -> None:
    asset = node_id  # the runtime passes the spec id; it IS the asset name
    chart_id = node_id[len("ofgem-") :]
    token = ENTITY_TOKENS[chart_id]
    js = _fetch_inject(token)
    options = _extract_options(js)
    data = options.get("data") or {}
    csv_text = data.get("csv")
    if not csv_text:
        raise ValueError(f"{node_id}: everviz options has no data.csv")
    rows = _csv_to_long(csv_text)
    save_raw_ndjson(rows, asset)


DOWNLOAD_SPECS = [
    NodeSpec(
        id=f"ofgem-{eid.lower().replace('_', '-')}",
        fn=fetch_one,
        kind="download",
    )
    for eid in ENTITY_IDS
]
