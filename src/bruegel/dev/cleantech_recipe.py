"""
Bruegel European Clean Tech Tracker - parsing recipe.

The old page https://www.bruegel.org/dataset/european-clean-tech-tracker now links to
the live app at https://european-clean-tech-tracker.bruegel.org/ (a Next.js App Router
site). There is NO downloadable file and NO JSON API.

Data is server-rendered and inlined in the React Server Component (RSC) payloads.
Fetch a route with header "RSC: 1" (or ?_rsc=<id>) -> text/x-component stream.
Inside, chart components carry data as Highcharts configs:
    {"data":{ "<chartKey>": {"categories":[...], "series":[{"name","data":[...]}, ...]}, ...}}

Routes that carry tidy (categories x series) chart data include /investments/overview.
This recipe targets /investments/overview (EU clean-tech investment by destination
country x project status), the cleanest published table, and flattens to long.

To rediscover routes: GET https://european-clean-tech-tracker.bruegel.org/ with header
"RSC:1" and read the route segment URLs in the payload, or use the nav links.
"""
import httpx, json, re

BASE = "https://european-clean-tech-tracker.bruegel.org"
HDRS = {"User-Agent": "Mozilla/5.0", "RSC": "1"}


def fetch_rsc(path):
    r = httpx.get(BASE + path, headers=HDRS, timeout=60, follow_redirects=True)
    r.raise_for_status()
    return r.text


def _match_brace(s, start):
    """Return index of the '}' matching the '{' at position `start`."""
    depth = 0
    i = start
    instr = False
    esc = False
    while i < len(s):
        c = s[i]
        if esc:
            esc = False
        elif c == "\\":
            esc = True
        elif c == '"':
            instr = not instr
        elif not instr:
            if c == "{":
                depth += 1
            elif c == "}":
                depth -= 1
                if depth == 0:
                    return i
        i += 1
    return -1


def extract_chart_objects(rsc):
    """Find every {"categories":[...], "series":[...]} object anywhere in the RSC."""
    charts = []
    for m in re.finditer(r'\{"categories"', rsc):
        start = m.start()
        end = _match_brace(rsc, start)
        if end < 0:
            continue
        block = rsc[start : end + 1].replace('"$undefined"', "null")
        try:
            obj = json.loads(block)
        except json.JSONDecodeError:
            continue
        if "categories" in obj and "series" in obj:
            charts.append(obj)
    return charts


def flatten(rows, route, chart_index, chart):
    cats = chart["categories"]
    for s in chart["series"]:
        name = s.get("name")
        data = s.get("data") or []
        for cat, val in zip(cats, data):
            rows.append({
                "route": route,
                "chart_index": chart_index,
                "category": cat,      # entity (country / quarter / tech)
                "series": name,       # status / tech / metric
                "value": val,
            })


def main(route="/investments/overview"):
    rsc = fetch_rsc(route)
    charts = extract_chart_objects(rsc)
    rows = []
    for i, ch in enumerate(charts):
        flatten(rows, route, i, ch)
    return rows, charts


if __name__ == "__main__":
    rows, charts = main()
    print("CHARTS FOUND:", len(charts))
    for i, ch in enumerate(charts):
        print(f"  chart {i}: categories={ch['categories'][:4]}{'...' if len(ch['categories'])>4 else ''} "
              f"series={[s.get('name') for s in ch['series']]}")
    print("\nTOTAL ROWS:", len(rows))
    print("\nSAMPLE 5 ROWS:")
    for r in rows[:5]:
        print(r)
