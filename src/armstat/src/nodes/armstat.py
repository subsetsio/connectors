"""Armstat (Statistical Committee of the Republic of Armenia) — ArmStatBank.

ArmStatBank is a PX-Web 25.1 instance whose JSON REST API is disabled, so each
.px statistical table is pulled through the server-rendered ASP.NET export UI
(research mechanism `pxweb_form_export`). One download node per rank-accepted
table; each is small enough to re-pull in full every run (stateless, no
watermark).

Per-table flow (one httpx client, cookies persist across the three calls):
  1. GET the table deep-link page -> scrape ASP.NET hidden fields
     (__VIEWSTATE / __VIEWSTATEGENERATOR / __EVENTVALIDATION) and every
     <select ...ValuesListBox> with all of its option values (one listbox per
     dimension).
  2. POST those hidden fields + every option value of every listbox (= select
     ALL values = the full table) + the ButtonViewTable trigger. PX-Web replies
     302 and stores the selection server-side against the session cookies.
  3. GET <table>/table/tableViewLayout1/?downloadfile=FileTypeJsonStat2 -> the
     full JSON-stat 2.0 cube.

The cube is flattened to long format (one row per cell: a column per dimension
carrying the value *label*, plus a numeric `value`) and saved as NDJSON because
the dimension set differs from table to table (heterogeneous schemas).
"""

import math
import re
import html as _html

import httpx
from tenacity import (
    retry,
    retry_if_exception,
    stop_after_attempt,
    wait_exponential,
)

from subsets_utils import (
    NodeSpec,
    SqlNodeSpec,
    get,
    post,
    save_raw_ndjson,
)
from subsets_utils.retry import is_transient
from constants import ASSET_PATHS, ENTITY_IDS

HOST = "https://statbank.armstat.am"
_TIMEOUT = 120.0
_VIEW_BTN = "ctl00$ContentPlaceHolderMain$VariableSelector1$VariableSelector1$ButtonViewTable"
_HIDDEN = ("__VIEWSTATE", "__VIEWSTATEGENERATOR", "__EVENTVALIDATION")


# ArmStatBank is an overloaded ASP.NET box that drops connections mid-stream:
# the prior full run failed 308/774 nodes on "[Errno 104] Connection reset by
# peer". httpx surfaces a reset *during the response read* as httpx.ReadError
# (and a reset while sending as httpx.WriteError) — both NetworkError/
# TransportError subclasses that the shared `transient_retry` predicate does
# NOT cover, so those nodes failed hard and, under DAG_ON_FAILURE=crash, killed
# the whole run. We retry the full transport-error family here (plus the
# standard 429/5xx via `is_transient`), with extra attempts for the flaky host.
def _armstat_transient(exc: BaseException) -> bool:
    return isinstance(exc, httpx.TransportError) or is_transient(exc)


def armstat_retry(*, attempts: int = 8, min_wait: float = 4, max_wait: float = 120):
    return retry(
        retry=retry_if_exception(_armstat_transient),
        stop=stop_after_attempt(attempts),
        wait=wait_exponential(min=min_wait, max=max_wait),
        reraise=True,
    )


@armstat_retry()
def _get(url):
    resp = get(url, timeout=_TIMEOUT)
    resp.raise_for_status()
    return resp


@armstat_retry()
def _post(url, data):
    resp = post(url, data=data, timeout=_TIMEOUT)
    resp.raise_for_status()
    return resp


def _hidden_fields(page: str) -> dict:
    out = {}
    for name in _HIDDEN:
        m = re.search(r'id="%s"[^>]*value="([^"]*)"' % name, page)
        out[name] = _html.unescape(m.group(1)) if m else ""
    return out


def _listbox_selection(page: str) -> dict:
    """Map each variable's ValuesListBox control name -> list of all its option
    values (selecting every value = the full table)."""
    sel = {}
    for name, body in re.findall(
        r'<select[^>]*name="([^"]*ValuesListBox)"[^>]*>(.*?)</select>', page, re.S
    ):
        vals = [_html.unescape(v) for v in re.findall(r'<option[^>]*value="([^"]*)"', body)]
        if vals:
            sel[_html.unescape(name)] = vals
    return sel


def _col_name(code, used):
    """Sanitize a PX-Web dimension code into a stable, unique column name,
    avoiding the reserved measure column."""
    name = re.sub(r"[^0-9A-Za-z]+", "_", str(code)).strip("_").lower()
    if not name:
        name = "dim"
    if name == "value":
        name = "value_dim"
    base, n = name, 2
    while name in used:
        name = f"{base}_{n}"
        n += 1
    used.add(name)
    return name


def _coerce(v):
    if isinstance(v, (int, float)):
        return v
    if isinstance(v, str):
        try:
            return float(v)
        except ValueError:
            return None
    return None


def _decode(dataset, colmap):
    """Flatten a JSON-stat 2.0 dataset to long-format rows."""
    dim = dataset["dimension"]
    meta = ("id", "size", "role")
    order = dataset.get("id") or dim.get("id") or [k for k in dim if k not in meta]
    sizes = dataset.get("size") or dim.get("size") or [
        len(dim[d]["category"]["index"]) for d in order
    ]
    pos_label = {}
    for d in order:
        cat = dim[d]["category"]
        index = cat["index"]
        # index may be a dict {code: pos} or a list [code, ...]
        if isinstance(index, dict):
            arr = [None] * len(index)
            for code, pos in index.items():
                arr[pos] = code
        else:
            arr = list(index)
        labels = cat.get("label", {})
        pos_label[d] = [labels.get(code, code) for code in arr]

    values = dataset["value"]
    if isinstance(values, dict):
        n = math.prod(sizes) if sizes else 0
        dense = [None] * n
        for k, v in values.items():
            dense[int(k)] = v
        values = dense

    rows = []
    for idx, raw in enumerate(values):
        rem = idx
        row = {}
        for k in range(len(order) - 1, -1, -1):
            d = order[k]
            s = sizes[k]
            row[colmap[d]] = pos_label[d][rem % s]
            rem //= s
        row["value"] = _coerce(raw)
        rows.append(row)
    return rows


def fetch_one(node_id: str) -> None:
    asset = node_id  # the spec id IS the asset name
    base = HOST + ASSET_PATHS[node_id]

    page = _get(base).text
    fields = _hidden_fields(page)
    listboxes = _listbox_selection(page)
    if not listboxes:
        raise RuntimeError(f"{node_id}: no variable listboxes found on {base}")

    form = {**fields, _VIEW_BTN: "View table", "__EVENTTARGET": "", "__EVENTARGUMENT": ""}
    form.update(listboxes)  # httpx encodes list values as repeated fields
    _post(base, form)  # 302 -> result page; selection stored against session cookie

    dl = base + "table/tableViewLayout1/?downloadfile=FileTypeJsonStat2"
    resp = _get(dl)
    ctype = resp.headers.get("content-type", "")
    if "json" not in ctype.lower():
        raise RuntimeError(
            f"{node_id}: expected JSON-stat from {dl}, got content-type {ctype!r} "
            f"(selection/export likely failed)"
        )
    dataset = resp.json()
    if not isinstance(dataset, dict) or "dimension" not in dataset or "value" not in dataset:
        raise RuntimeError(f"{node_id}: unexpected JSON-stat shape from {dl}")

    # Dimension *codes* are often Armenian; the English dimension *label* makes a
    # far better column name. Fall back to the code when no label is published.
    dim = dataset["dimension"]
    order = dataset.get("id") or list(dim.keys())
    used = set()
    colmap = {d: _col_name(dim[d].get("label") or d, used) for d in order}
    rows = _decode(dataset, colmap)
    save_raw_ndjson(rows, asset)


DOWNLOAD_SPECS = [
    NodeSpec(id=eid, fn=fetch_one, kind="download") for eid in ENTITY_IDS
]

# One published Delta table per source table: thin parse pass — type the measure
# and drop empty cells. Dimension columns pass through as the source's labels.
TRANSFORM_SPECS = [
    SqlNodeSpec(
        id=f"{s.id}-transform",
        deps=[s.id],
        sql=f'''
            SELECT * EXCLUDE (value), CAST(value AS DOUBLE) AS value
            FROM "{s.id}"
            WHERE value IS NOT NULL
        ''',
    )
    for s in DOWNLOAD_SPECS
]
