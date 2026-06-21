"""SGS series catalog — discovered via the CKAN open-data portal.

The SGS REST surface (https://api.bcb.gov.br/dados/serie) is a flat time-series
API keyed by numeric series code; there is no native catalog, so the set of
series is discovered from CKAN (https://dadosabertos.bcb.gov.br). This module
owns that discovery — `sgs_values` imports `_discover_sgs_series` from here, so
the series→values relationship is an explicit import, not a buried duplicate.
"""
import re

from subsets_utils import NodeSpec, SqlNodeSpec, save_raw_ndjson

from utils import SLUG, _fetch_json

CKAN = "https://dadosabertos.bcb.gov.br/api/3/action"

_SGS_CODE_RE = re.compile(r"bcdata\.sgs\.(\d+)", re.I)


def _discover_sgs_series() -> list[dict]:
    """Enumerate SGS series from the CKAN portal.

    A series is any package exposing a resource whose URL embeds
    `bcdata.sgs.<code>`. Returns sorted unique {code, name, title}.
    """
    found: dict[int, dict] = {}
    start = 0
    rows = 1000
    while True:
        res = _fetch_json(f"{CKAN}/package_search",
                          {"q": "sgs", "rows": rows, "start": start})["result"]
        results = res.get("results", [])
        if not results:
            break
        for p in results:
            for rsc in p.get("resources", []):
                m = _SGS_CODE_RE.search(rsc.get("url", "") or "")
                if m:
                    code = int(m.group(1))
                    found.setdefault(code, {
                        "code": code,
                        "name": p.get("name"),
                        "title": p.get("title"),
                    })
                    break
        start += len(results)
        if start >= res.get("count", 0):
            break
    return [found[c] for c in sorted(found)]


def fetch_sgs_series(node_id: str) -> None:
    """Stateless full pull of the SGS series catalog (one row per series)."""
    save_raw_ndjson(_discover_sgs_series(), node_id)


DOWNLOAD_SPECS = [
    NodeSpec(id=f"{SLUG}-sgs-series", fn=fetch_sgs_series, kind="download"),
]

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id=f"{SLUG}-sgs-series-transform",
        deps=[f"{SLUG}-sgs-series"],
        sql=f'SELECT * FROM "{SLUG}-sgs-series"',
    ),
]
