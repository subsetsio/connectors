"""Bank of Finland / FIN-FSA open-data Timeseries API (v4) connector.

Mechanism: rest_v4 — https://api.boffsaopendata.fi/v4 (Azure APIM, no auth).
Each of the 8 datasets is a distinct SDMX-style dataflow with its own dimension
structure. Fetch strategy is stateless full re-pull (per the implement guide's
default): the whole corpus is ~2820 series and re-pulls in minutes, so there is
no watermark/cursor — revisions are picked up for free.

For each dataset we enumerate every series via /series/{ds} (paginated with
pageNumber; the gateway truncates responses larger than ~1.96MB, so we keep
pages small), then pull full history via
/observations/{ds}?seriesName=<semicolon-batch>&pageSize=9999. Series are
batched by URL length, not a fixed count: the gateway returns 404 for request
URLs longer than ~2KB, and key lengths vary across datasets. Raw is written as
NDJSON because the dimension columns differ across datasets; within one dataset
they are consistent, so the per-dataset transform reads them as columns.
Data licensed CC-BY 4.0.
"""

from urllib.parse import quote

from subsets_utils import NodeSpec, SqlNodeSpec, get, save_raw_ndjson, transient_retry

from constants import ENTITY_IDS

BASE = "https://api.boffsaopendata.fi/v4"
SLUG = "bank-of-finland"
SERIES_PAGE_SIZE = 100     # ~0.6MB/page, safely under the ~1.96MB response cap
OBS_PAGE_SIZE = 9999       # observations items per page (one batch fits in a page)
MAX_SERIESNAME_CHARS = 1500  # encoded seriesName budget; total URL stays < ~1.6KB (<2KB gateway cap)


@transient_retry()
def _get_json(path, params):
    resp = get(BASE + path, params=params, timeout=(10.0, 120.0))
    resp.raise_for_status()
    return resp.json()


def _en(descriptions):
    """English description for a dimension code, or None if absent/blank."""
    for d in descriptions or []:
        if d.get("lang") == "en":
            return d.get("description") or None
    return None


def _dataset_for_node(node_id):
    """Recover the original dataset code from the spec id."""
    suffix = node_id[len(SLUG) + 1:]
    for eid in ENTITY_IDS:
        if eid.lower().replace("_", "-") == suffix:
            return eid
    raise ValueError(f"no dataset maps to node id {node_id!r}")


def _fetch_series(dataset):
    """name -> {'title': str, 'dims': {DIM_NAME: (code, en_label)}} for every series."""
    meta = {}
    page = 1
    while True:
        j = _get_json(
            f"/series/{dataset}",
            {"pageSize": SERIES_PAGE_SIZE, "pageNumber": page},
        )
        for it in j["items"]:
            dims = {}
            for d in it.get("dimensions", []):
                dims[d["name"]] = (d.get("value"), _en(d.get("descriptions")))
            meta[it["name"]] = {"title": it.get("title"), "dims": dims}
        total_pages = j.get("totalPages", 1)
        if j.get("currentPage", page) >= total_pages:
            break
        page += 1
        if page > total_pages + 1:  # safety ceiling: never loop unbounded
            raise RuntimeError(f"{dataset}: series pagination did not terminate")
    return meta


def _batch_by_url_length(names):
    """Group series names into semicolon-joinable batches whose encoded length
    stays under the gateway's URL cap (it 404s on URLs longer than ~2KB)."""
    batches, cur, cur_len = [], [], 0
    for name in names:
        enc = len(quote(name, safe="")) + 3  # +3 for an encoded ';' separator
        if cur and cur_len + enc > MAX_SERIESNAME_CHARS:
            batches.append(cur)
            cur, cur_len = [], 0
        cur.append(name)
        cur_len += enc
    if cur:
        batches.append(cur)
    return batches


def fetch_one(node_id):
    asset = node_id  # the spec id IS the asset name
    dataset = _dataset_for_node(node_id)

    series_meta = _fetch_series(dataset)
    names = list(series_meta)
    if not names:
        raise RuntimeError(f"{dataset}: /series returned no series")

    rows = []
    for batch in _batch_by_url_length(names):
        j = _get_json(
            f"/observations/{dataset}",
            {"seriesName": ";".join(batch), "pageSize": OBS_PAGE_SIZE},
        )
        if j.get("totalPages", 1) > 1:
            raise RuntimeError(
                f"{dataset}: observations batch spans {j['totalPages']} pages; "
                "reduce MAX_SERIESNAME_CHARS"
            )
        for item in j["items"]:
            sname = item["name"]
            m = series_meta.get(sname, {"title": None, "dims": {}})
            dim_cols = {}
            for dname, (code, en) in m["dims"].items():
                dim_cols[dname] = code
                dim_cols[f"{dname}_en"] = en
            for o in item.get("observations", []):
                row = {
                    "series": sname,
                    "title": m["title"],
                    "period": o.get("period"),
                    "period_code": o.get("periodCode"),
                    "value": o.get("value"),
                }
                row.update(dim_cols)
                rows.append(row)

    if not rows:
        raise RuntimeError(f"{dataset}: no observations fetched across {len(names)} series")

    save_raw_ndjson(rows, asset)


DOWNLOAD_SPECS = [
    NodeSpec(
        id=f"{SLUG}-{eid.lower().replace('_', '-')}",
        fn=fetch_one,
        kind="download",
    )
    for eid in ENTITY_IDS
]


# One published long-format Delta table per dataset. The dimension columns differ
# per dataset, so the transform is generic: pass everything through, drop nulls,
# and type the period/value pair. (* EXCLUDE keeps the per-dataset dimension cols.)
TRANSFORM_SPECS = [
    SqlNodeSpec(
        id=f"{s.id}-transform",
        deps=[s.id],
        sql=f'''
            SELECT
                * EXCLUDE (period, value),
                CAST(period AS DATE)  AS date,
                CAST(value AS DOUBLE) AS value
            FROM "{s.id}"
            WHERE value IS NOT NULL
        ''',
    )
    for s in DOWNLOAD_SPECS
]
