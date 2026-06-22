import sys
sys.path.insert(0, "src")
from collections import Counter
from subsets_utils import configure_http
from nodes.w3techs import _parse_view, _VIEWS, CATEGORIES

configure_http(headers={"User-Agent": "subsets.io-connector/1.0 (+https://subsets.io)"})

# one both, one ms-only, one all-only, one big
for slug in ["content_management", "web_server", "image_format", "server_location"]:
    name = CATEGORIES[slug]
    allrows = []
    for view, metric in _VIEWS:
        rows = _parse_view(slug, name, view, metric)
        allrows.extend(rows)
        print(f"{slug:20} {view:6} ({metric:12}) -> {len(rows)} rows")
    if allrows:
        dates = sorted({r['date'] for r in allrows})
        print(f"   metrics={dict(Counter(r['metric'] for r in allrows))} "
              f"date_range={dates[0]}..{dates[-1]} techs={len({r['technology'] for r in allrows})}")
        print(f"   sample: {allrows[0]}")
    print()
