"""PORDATA connector — Portugal national statistical indicators.

PORDATA (Fundacao Francisco Manuel dos Santos) is an OutSystems web app with no
machine-readable data API. Each indicator is published as its own page at
`https://www.pordata.pt/en/portugal/<slug>-<id>` whose server-rendered HTML
embeds the full time-series table (verified: a plain GET returns the complete
`<table>`, no JS/XHR needed). One indicator page = one publishable subset.

Scope: this connector serves the **Portugal national** indicators only. The
sibling /europe/ and /municipalities/ trees render their tables exclusively via
interactive OutSystems AJAX postbacks (a "table" view toggle backed by
`__OSVSTATE`) that are not reliably replayable outside a browser; those entities
are gated below the publish threshold in rank for a future interactive fetcher.

Each indicator's HTML table is time-down-the-rows, dimensions-across-the-columns,
with a heterogeneous (per-indicator) column list. To keep one uniform SQL
transform per subset, the fetch normalizes every table into a generic LONG shape
-- (period, series, series_group, value) -- and the transform is a thin
cast/clean pass. Re-fetch is a full re-pull each run (stateless): the source has
no incremental filter and a page is a single cheap GET.
"""

import re

import pyarrow as pa
from lxml import html as lh

from constants import ENTITY_IDS, ENTITY_SLUGS
from subsets_utils import NodeSpec, SqlNodeSpec, get, save_raw_ndjson, transient_retry

BASE = "https://www.pordata.pt/en/portugal"
NUM_RE = re.compile(r"-?\d[\d,]*\.?\d*")


@transient_retry()  # 6 attempts, exp backoff; retries 429/5xx/transient network
def _get_page(url):
    resp = get(url, timeout=(10.0, 120.0))
    resp.raise_for_status()
    return resp.text


def _find_data_table(doc):
    """The indicator data table is the non-script <table> with the most numeric
    content. Pages also carry small layout/symbology tables; those lose on digits."""
    best, best_digits = None, 0
    for t in doc.xpath("//table"):
        if any(a.tag in ("script", "style", "head") for a in t.iterancestors()):
            continue
        if len(t.xpath(".//tr")) < 4:
            continue
        digits = len(NUM_RE.findall(t.text_content()))
        if digits > best_digits:
            best, best_digits = t, digits
    return best


def _expand(cells):
    """Flatten a header row honoring colspan -> one label per spanned column."""
    out = []
    for c in cells:
        try:
            span = int(c.get("colspan") or 1)
        except ValueError:
            span = 1
        out.extend([c.text_content().strip()] * span)
    return out


def _parse_value(text):
    """Pull the numeric out of a cell. Cells may carry footnote prefixes like
    'Pro'/'Pre' (provisional/preliminary) or symbology markers; non-numeric
    cells ('x', '//', empty) yield None and are dropped in the transform."""
    t = (text or "").strip()
    if not t:
        return None
    m = NUM_RE.search(t)
    if not m:
        return None
    try:
        return float(m.group(0).replace(",", ""))
    except ValueError:
        return None


def _parse_indicator(html_text):
    """Normalize one indicator page's HTML table into long-format records."""
    doc = lh.fromstring(html_text)
    t = _find_data_table(doc)
    if t is None:
        return []
    rows = t.xpath(".//tr")
    header_rows, data_rows = [], []
    for r in rows:
        cells = r.xpath("./td|./th")
        if cells and all(c.tag == "th" for c in cells):
            header_rows.append(cells)
        elif r.xpath("./td"):
            data_rows.append(r.xpath("./td"))
    if not header_rows or not data_rows:
        return []
    ncol = max(len(d) for d in data_rows)
    value_cols = ncol - 1  # column 0 is the time period; the rest are values
    if value_cols < 1:
        return []

    # Leaf column labels: the header row whose width matches the value columns.
    leaf, period_name = None, "period"
    for h in header_rows:
        exp = _expand(h)
        if len(exp) == value_cols:
            leaf = exp
            break
    if leaf is None:
        # Single-level header (e.g. ['Years','GDP']): first cell names the
        # period axis, the rest are the value labels.
        exp = _expand(header_rows[-1])
        if len(exp) >= value_cols + 1:
            period_name = exp[0]
            leaf = exp[1:value_cols + 1]
        else:
            leaf = (exp + [""] * value_cols)[:value_cols]
    else:
        period_name = header_rows[0][0].text_content().strip() or "period"

    # Group labels come from the top header row (the category band), offset by
    # the leading period column.
    group = [None] * value_cols
    if len(header_rows) >= 2:
        top = _expand(header_rows[0])
        grp = top[1:value_cols + 1] if len(top) >= value_cols + 1 else top[:value_cols]
        for i in range(min(value_cols, len(grp))):
            g = grp[i].strip()
            group[i] = g or None

    recs = []
    for d in data_rows:
        period = d[0].text_content().strip()
        for j in range(min(value_cols, len(d) - 1)):
            txt = d[j + 1].text_content().strip()
            recs.append({
                "period": period,
                "period_name": period_name,
                "series": leaf[j] if j < len(leaf) else "",
                "series_group": group[j],
                "value_text": txt,
                "value": _parse_value(txt),
            })
    return recs


def fetch_one(node_id: str) -> None:
    """Fetch and normalize one Portugal indicator page. The runtime passes the
    spec id (which is also the raw asset name); recover the collect entity by
    stripping the 'pordata-' prefix and look its slug up in ENTITY_SLUGS."""
    asset = node_id
    entity_id = node_id[len("pordata-"):]          # e.g. 'portugal-10'
    indicator_id = int(entity_id.rsplit("-", 1)[1])
    slug = ENTITY_SLUGS[entity_id]
    url = f"{BASE}/{slug}-{indicator_id}"

    recs = _parse_indicator(_get_page(url))

    schema = pa.schema([
        ("indicator_id", pa.int64()),
        ("period", pa.string()),
        ("period_name", pa.string()),
        ("series", pa.string()),
        ("series_group", pa.string()),
        ("value_text", pa.string()),
        ("value", pa.float64()),
    ])
    for r in recs:
        r["indicator_id"] = indicator_id
    table = pa.Table.from_pylist(recs, schema=schema)
    save_raw_ndjson(table.to_pylist(), asset)


DOWNLOAD_SPECS = [
    NodeSpec(
        id=f"pordata-{eid.lower().replace('_', '-')}",
        fn=fetch_one,
        kind="download",
    )
    for eid in ENTITY_IDS
]

# One published Delta table per indicator. Thin cast/clean pass: keep numeric
# cells only, expose a parsed integer `year` alongside the raw period string.
TRANSFORM_SPECS = [
    SqlNodeSpec(
        id=f"{s.id}-transform",
        deps=[s.id],
        temporal="period",
        sql=f'''
            SELECT
                CAST(indicator_id AS INTEGER)        AS indicator_id,
                period,
                TRY_CAST(period AS INTEGER)          AS "year",
                series,
                series_group,
                CAST(value AS DOUBLE)                AS value
            FROM "{s.id}"
            WHERE value IS NOT NULL
              AND series IS NOT NULL
        ''',
    )
    for s in DOWNLOAD_SPECS
]
