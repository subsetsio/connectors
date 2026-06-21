"""
Bruegel China Economic Database - parsing recipe.

The dashboard at https://www.bruegel.org/dataset/china-economic-database embeds a
Plotly Dash app hosted at https://china-dashboard.herokuapp.com/.

There is NO downloadable file. Data lives inside Dash callback responses as Plotly
figures. We:
  1. GET /_dash-update-component routing callback with pathname="/" to discover page paths.
  2. For each page, POST the routing callback to render that page's content.
  3. Walk the returned component tree, collect every dcc.Graph 'figure'.
  4. Flatten each figure's traces (x, y, name) into long rows.
"""
import httpx, json, re, time

BASE = "https://china-dashboard.herokuapp.com"
H = {"Content-Type": "application/json"}

ROUTE_BODY = lambda path: {
    "output": ".._pages_content.children..._pages_store.data..",
    "outputs": [
        {"id": "_pages_content", "property": "children"},
        {"id": "_pages_store", "property": "data"},
    ],
    "inputs": [
        {"id": "_pages_location", "property": "pathname", "value": path},
        {"id": "_pages_location", "property": "search", "value": ""},
    ],
    "changedPropIds": ["_pages_location.pathname"],
}


def route(client, path, retries=5):
    # Heroku free dyno occasionally returns transient 500s; retry with backoff.
    for attempt in range(retries):
        r = client.post(BASE + "/_dash-update-component", json=ROUTE_BODY(path), headers=H, timeout=60)
        if r.status_code == 200:
            return r.json()["response"]["_pages_content"]["children"]
        time.sleep(2 * (attempt + 1))
    r.raise_for_status()


def discover_pages(client):
    home = route(client, "/")
    return sorted(set(re.findall(r'"href":\s*"(/[^"]*)"', json.dumps(home))))


def collect_graphs(node, out):
    if isinstance(node, dict):
        if node.get("type") == "Graph":
            fig = node.get("props", {}).get("figure")
            if fig:
                out.append(fig)
        for v in node.values():
            collect_graphs(v, out)
    elif isinstance(node, list):
        for v in node:
            collect_graphs(v, out)


def title_of(fig):
    t = (fig.get("layout") or {}).get("title")
    if isinstance(t, dict):
        return t.get("text")
    return t


def flatten(rows, page, fig):
    chart = title_of(fig)
    for tr in fig.get("data", []):
        series = tr.get("name")
        x = tr.get("x") or []
        y = tr.get("y") or []
        # bar charts may use x=categories,y=values; line charts x=dates
        for xi, yi in zip(x, y):
            rows.append({
                "page": page,
                "chart": chart,
                "series": series,
                "x": xi,
                "value": yi,
            })


def main():
    rows = []
    with httpx.Client(headers={"User-Agent": "Mozilla/5.0"}) as client:
        pages = discover_pages(client)
        for p in pages:
            content = route(client, p)
            figs = []
            collect_graphs(content, figs)
            for f in figs:
                flatten(rows, p, f)
    return rows


if __name__ == "__main__":
    rows = main()
    print("TOTAL ROWS:", len(rows))
    print("PAGES:", len(set(r["page"] for r in rows)))
    print("CHARTS:", len(set((r["page"], r["chart"]) for r in rows)))
    print("\nSAMPLE 5 ROWS:")
    for r in rows[:5]:
        print(r)
