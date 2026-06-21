"""Global Fund connector — OData v4.2 entity-set snapshots.

Mechanism: the Global Fund Data Service v4 OData API, root
``https://fetch.theglobalfund.org/v4.2/odata/`` (anonymous, JSON).

Shape: stateless full re-pull. Each refresh re-fetches the whole entity set and
overwrites. The corpus is modest — the largest set, AllFinancialIndicators, is
~1.24M rows; the rest are well under 20k — and the service exposes no delta
filter useful for our whole-snapshot pattern, so we re-pull in full every run.
Revisions and late corrections are picked up for free (no stored watermark).
Rows are streamed page-by-page into gzip NDJSON so peak memory stays bounded to
one page (~20k records) rather than the whole table.

OData quirks (verified during research + probing):
- No server-driven ``@odata.nextLink`` paging — caller pages with ``$top``/``$skip``.
- ``$top`` >= ~50000 silently returns an EMPTY ``value`` array (no error). We
  page at 20000.
- The advertised path ``data-service.theglobalfund.org/api/v4/odata`` 301s to a
  broken double-slash URL; we hit ``fetch.theglobalfund.org/v4.2/odata`` directly.
- No CSV/XML output — JSON only.
"""

from subsets_utils import NodeSpec, SqlNodeSpec, get, save_raw_ndjson, transient_retry

from constants import ENTITY_IDS

BASE = "https://fetch.theglobalfund.org/v4.2/odata"
PAGE = 20000  # server returns an empty page for $top >= ~50000

# spec-id suffix (lowercased entity) -> OData entity-set name (case-sensitive).
ENTITY_SETS = {eid.lower().replace("_", "-"): eid for eid in ENTITY_IDS}

# Absolute safety ceiling on pages. Largest set ~1.24M rows -> ~62 pages; 1000
# pages (20M rows) means the source grew enormously or paging is looping — fail
# loudly rather than crawl forever.
MAX_PAGES = 1000


@transient_retry()
def _get_json(url, params=None):
    resp = get(url, params=params, timeout=(10.0, 300.0))
    resp.raise_for_status()
    return resp.json()


@transient_retry()
def _get_count(entity_set):
    resp = get(f"{BASE}/{entity_set}/$count", timeout=(10.0, 120.0))
    resp.raise_for_status()
    return int(resp.text.strip())


def _entity_set_for(node_id):
    return ENTITY_SETS[node_id[len("global-fund-"):]]


def _iter_rows(entity_set, expected):
    """Yield every row of an entity set, paging with $top/$skip.

    Raises rather than returns short: a silent truncation (empty page hit early,
    or paging cap) would publish a partial snapshot, which is worse than failing.
    """
    skip = 0
    seen = 0
    pages = 0
    while True:
        if pages >= MAX_PAGES:
            raise RuntimeError(
                f"{entity_set}: exceeded MAX_PAGES={MAX_PAGES} at skip={skip} "
                f"(expected ~{expected} rows) — source grew or paging looped"
            )
        page = _get_json(f"{BASE}/{entity_set}", {"$top": PAGE, "$skip": skip})
        rows = page.get("value", [])
        if not rows:
            break
        for row in rows:
            yield row
        seen += len(rows)
        pages += 1
        skip += PAGE
    # $count is a snapshot taken just before the crawl; allow small drift from
    # concurrent edits but trip on a real shortfall (>5%).
    if expected and seen < expected * 0.95:
        raise RuntimeError(
            f"{entity_set}: pulled {seen} rows but $count reported {expected} "
            f"(>5% short) — pagination likely truncated"
        )


def fetch_one(node_id: str) -> None:
    asset = node_id  # the runtime passes the spec id; it IS the asset name
    entity_set = _entity_set_for(node_id)
    expected = _get_count(entity_set)
    save_raw_ndjson(_iter_rows(entity_set, expected), asset, compression="gzip")


DOWNLOAD_SPECS = [
    NodeSpec(
        id=f"global-fund-{eid.lower().replace('_', '-')}",
        fn=fetch_one,
        kind="download",
    )
    for eid in ENTITY_IDS
]

# One published Delta table per entity set. OData properties are type-consistent
# across rows (the source enforces a CSDL schema), so a straight pass-through is
# safe; DuckDB's read_json_auto types each column. The transform is still the
# correctness gate — a 0-row result fails the node.
TRANSFORM_SPECS = [
    SqlNodeSpec(
        id=f"{s.id}-transform",
        deps=[s.id],
        sql=f'SELECT * FROM "{s.id}"',
    )
    for s in DOWNLOAD_SPECS
]
