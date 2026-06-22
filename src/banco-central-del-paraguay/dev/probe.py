import os
import re
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from subsets_utils import get

UA = {"User-Agent": "Mozilla/5.0 (compatible; subsets-bot/1.0)"}


def fetch(url):
    r = get(url, headers=UA, timeout=(10.0, 60.0))
    print("URL", url, "->", r.status_code, "len", len(r.text))
    return r.text


def rows(html):
    out = []
    for tr in re.findall(r"<tr.*?</tr>", html, re.S):
        cells = re.findall(r"<t[dh][^>]*>(.*?)</t[dh]>", tr, re.S)
        cells = [re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", c)).strip() for c in cells]
        out.append(cells)
    return out


print("=== monedas-mensual 2014/5 ===")
h = fetch("https://www.bcp.gov.py/webapps/web/cotizacion/monedas-mensual?anho=2014&mes=5")
for r in rows(h)[:8]:
    print(r)

print("\n=== monedas-historica (USD, default) ===")
h = fetch("https://www.bcp.gov.py/webapps/web/cotizacion/monedas-historica")
# look for form inputs/selects to discover params
for m in re.findall(r"<(select|input)[^>]*name=\"([^\"]+)\"[^>]*>", h):
    print("FORM FIELD:", m)
# look for option values in moneda select
sel = re.search(r"<select[^>]*name=\"[^\"]*moneda[^\"]*\".*?</select>", h, re.S | re.I)
if sel:
    print("MONEDA OPTIONS:", re.findall(r"<option[^>]*value=\"([^\"]*)\"[^>]*>([^<]*)", sel.group(0))[:8])
for r in rows(h)[:6]:
    print(r)

print("\n=== monedas-historica with anho param ===")
h = fetch("https://www.bcp.gov.py/webapps/web/cotizacion/monedas-historica?anho=2020&idtipform=4")
for r in rows(h)[:6]:
    print(r)

print("\n=== referencial-fluctuante/anual ===")
h = fetch("https://www.bcp.gov.py/webapps/web/cotizacion/referencial-fluctuante/anual?anho=2020")
for r in rows(h)[:6]:
    print(r)
for m in re.findall(r"<(select|input)[^>]*name=\"([^\"]+)\"[^>]*>", h):
    print("FORM FIELD:", m)
