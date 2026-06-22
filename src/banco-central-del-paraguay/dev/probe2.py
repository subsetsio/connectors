import os
import re
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from subsets_utils import get

UA = {"User-Agent": "Mozilla/5.0 (compatible; subsets-bot/1.0)"}


def fetch(url):
    r = get(url, headers=UA, timeout=(10.0, 60.0))
    return r.text


def options(html, name):
    sel = re.search(r"<select[^>]*name=\"" + name + r"\".*?</select>", html, re.S | re.I)
    if not sel:
        return None
    return re.findall(r"<option[^>]*value=\"([^\"]*)\"[^>]*>([^<]*)", sel.group(0))


def tables(html):
    return re.findall(r"<table.*?</table>", html, re.S)


def first_rows(tbl, n=3):
    out = []
    for tr in re.findall(r"<tr.*?</tr>", tbl, re.S)[:n]:
        cells = re.findall(r"<t[dh][^>]*>(.*?)</t[dh]>", tr, re.S)
        cells = [re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", c)).strip() for c in cells]
        out.append(cells)
    return out


print("=== monedas-mensual anho options ===")
h = fetch("https://www.bcp.gov.py/webapps/web/cotizacion/monedas-mensual?anho=2014&mes=5")
print("anho:", options(h, "anho"))
print("mes:", options(h, "mes"))

print("\n=== monedas-historica anho options + table count ===")
h = fetch("https://www.bcp.gov.py/webapps/web/cotizacion/monedas-historica?anho=2020&moneda=USD")
print("anho:", (options(h, "anho") or [])[:3], "... last:", (options(h, "anho") or [])[-3:])
ts = tables(h)
print("num tables:", len(ts))
for i, t in enumerate(ts):
    print(f"  table {i} first rows:", first_rows(t, 2))

print("\n=== referencial-fluctuante/anual options + tables ===")
h = fetch("https://www.bcp.gov.py/webapps/web/cotizacion/referencial-fluctuante/anual?anho=2020")
print("anho:", (options(h, "anho") or [])[:3], "... last:", (options(h, "anho") or [])[-3:])
print("tipoOperacion:", options(h, "tipoOperacion"))
ts = tables(h)
print("num tables:", len(ts))
for i, t in enumerate(ts):
    print(f"  table {i} first rows:", first_rows(t, 2))

print("\n=== referencial-fluctuante/anual with tipoOperacion=V ===")
for tv in ["V", "2", "VENTA", "venta"]:
    h = fetch("https://www.bcp.gov.py/webapps/web/cotizacion/referencial-fluctuante/anual?anho=2020&tipoOperacion=" + tv)
    ts = tables(h)
    title = first_rows(ts[0], 1) if ts else None
    print(f"  tipoOperacion={tv}: title={title}")
