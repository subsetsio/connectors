"""China Economic Database — Plotly Dash app (no downloadable file). The routing
callback renders each page's component tree; every dcc.Graph figure holds the
data, flattened to long (page, chart, series, x, value)."""
import re

from subsets_utils import NodeSpec, SqlNodeSpec
from utils import clean, post_json, run_download

EID = "china-economic-database"
DEP = f"bruegel-{EID}"

_CHINA_BASE = "https://china-dashboard.herokuapp.com"
_CHINA_ROUTE_BODY = {
    "output": ".._pages_content.children..._pages_store.data..",
    "outputs": [
        {"id": "_pages_content", "property": "children"},
        {"id": "_pages_store", "property": "data"},
    ],
    "inputs": [
        {"id": "_pages_location", "property": "pathname", "value": None},
        {"id": "_pages_location", "property": "search", "value": ""},
    ],
    "changedPropIds": ["_pages_location.pathname"],
}


def _china_route(path):
    import copy
    body = copy.deepcopy(_CHINA_ROUTE_BODY)
    body["inputs"][0]["value"] = path
    return post_json(_CHINA_BASE + "/_dash-update-component", body)["response"]["_pages_content"]["children"]


def _china_collect_graphs(node, out):
    if isinstance(node, dict):
        if node.get("type") == "Graph":
            fig = node.get("props", {}).get("figure")
            if fig:
                out.append(fig)
        for v in node.values():
            _china_collect_graphs(v, out)
    elif isinstance(node, list):
        for v in node:
            _china_collect_graphs(v, out)


def _title_text(t):
    return t.get("text") if isinstance(t, dict) else t


def parse(_links):
    import json
    home = _china_route("/")
    pages = sorted(set(re.findall(r'"href":\s*"(/[^"]*)"', json.dumps(home))))
    out = []
    for p in pages:
        figs = []
        _china_collect_graphs(_china_route(p), figs)
        for fig in figs:
            layout = fig.get("layout") or {}
            chart = _title_text(layout.get("title"))
            # A page can carry two figures under the SAME title that plot the same
            # series in different units (e.g. "Trade in Goods" as USD Billion and as
            # YoY %). The y-axis title is the only thing separating them, so it is
            # part of the row's identity — without it the two collapse and `value`
            # silently mixes levels with growth rates.
            unit = _title_text((layout.get("yaxis") or {}).get("title"))
            for tr in fig.get("data", []):
                series = tr.get("name")
                for xi, yi in zip(tr.get("x") or [], tr.get("y") or []):
                    if yi is None or xi is None:  # a point with no observation label
                        continue
                    out.append({"page": p, "chart": chart, "series": series,
                                "unit": unit, "x": clean(xi), "value": clean(yi)})
    # A handful of traces plot the identical (x, y) point twice (e.g. the
    # 2023-07-19 policy rates, the 2025-06-10 steel output). The repeat carries no
    # observation, so drop exact duplicates — otherwise (page, chart, series, unit,
    # x) is not a row identity even though the dashboard shows one value per date.
    seen, deduped = set(), []
    for r in out:
        k = (r["page"], r["chart"], r["series"], r["unit"], str(r["x"]), r["value"])
        if k in seen:
            continue
        seen.add(k)
        deduped.append(r)
    return deduped


def fetch(node_id: str) -> None:
    run_download(node_id, None, parse)


DOWNLOAD_SPECS = [NodeSpec(id=DEP, fn=fetch, kind="download")]

_SQL = '''
        SELECT page, chart, series, x AS observation,
               TRY_CAST(value AS DOUBLE) AS value
        FROM "{dep}" WHERE TRY_CAST(value AS DOUBLE) IS NOT NULL
    '''

TRANSFORM_SPECS = [SqlNodeSpec(id=f"{DEP}-transform", deps=[DEP],
                               sql=_SQL.replace("{dep}", DEP))]
