"""Bank of Finland / FIN-FSA open-data Timeseries API (v4) connector.

Mechanism: rest_v4 — https://api.boffsaopendata.fi/v4 (Azure APIM, no auth).
Each of the 8 datasets is a distinct SDMX-style dataflow with its own dimension
structure. Fetch strategy is stateless full re-pull (per the implement guide's
default): the whole corpus is ~2820 series and re-pulls in minutes, so there is
no watermark/cursor — revisions are picked up for free.

For each dataset we enumerate every series via /series/{ds}?pageSize=9999 (one
page; we raise if the source ever exceeds it), then pull full history via
/observations/{ds}?seriesName=<semicolon-batch>&pageSize=9999. Raw is written as
NDJSON because the dimension columns differ across datasets; within one dataset
they are consistent, so the per-dataset transform reads them as columns.
Data licensed CC-BY 4.0.
"""

from subsets_utils import NodeSpec, SqlNodeSpec, get, save_raw_ndjson, transient_retry

from constants import ENTITY_IDS

BASE = "https://api.boffsaopendata.fi/v4"
SLUG = "bank-of-finland"
SERIES_BATCH = 40          # series per observations request (URL-length safe)
PAGE_SIZE = 9999           # >> max series in any single dataset


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
    j = _get_json(f"/series/{dataset}", {"pageSize": PAGE_SIZE})
    if j.get("totalPages", 1) > 1:
        # Safety ceiling: would silently truncate. Raise so source growth is visible.
        raise RuntimeError(
            f"{dataset}: series listing spans {j['totalPages']} pages at pageSize={PAGE_SIZE}; "
            "pagination must be implemented"
        )
    meta = {}
    for it in j["items"]:
        dims = {}
        for d in it.get("dimensions", []):
            dims[d["name"]] = (d.get("value"), _en(d.get("descriptions")))
        meta[it["name"]] = {"title": it.get("title"), "dims": dims}
    return meta


def fetch_one(node_id):
    asset = node_id  # the spec id IS the asset name
    dataset = _dataset_for_node(node_id)

    series_meta = _fetch_series(dataset)
    names = list(series_meta)
    if not names:
        raise RuntimeError(f"{dataset}: /series returned no series")

    rows = []
    for i in range(0, len(names), SERIES_BATCH):
        batch = names[i:i + SERIES_BATCH]
        j = _get_json(
            f"/observations/{dataset}",
            {"seriesName": ";".join(batch), "pageSize": PAGE_SIZE},
        )
        if j.get("totalPages", 1) > 1:
            raise RuntimeError(
                f"{dataset}: observations batch spans {j['totalPages']} pages; "
                "reduce SERIES_BATCH or paginate"
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
