import os
import re
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from subsets_utils import get

UA = {"User-Agent": "Mozilla/5.0 (compatible; subsets-bot/1.0)"}


def fetch(url):
    r = get(url, headers=UA, timeout=(10.0, 60.0))
    return r.status_code, r.text


def grid_has_data(html):
    """last table; count non-ND numeric cells in data rows."""
    ts = re.findall(r"<table.*?</table>", html, re.S)
    if not ts:
        return 0, None
    t = ts[-1]
    rows = re.findall(r"<tr.*?</tr>", t, re.S)
    n = 0
    title = None
    ts0 = re.findall(r"<table.*?</table>", html, re.S)[0]
    tr0 = re.findall(r"<tr.*?</tr>", ts0, re.S)
    if tr0:
        title = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", tr0[0])).strip()
    for tr in rows:
        cells = re.findall(r"<t[dh][^>]*>(.*?)</t[dh]>", tr, re.S)
        for c in cells:
            c = re.sub(r"<[^>]+>", "", c).strip()
            if re.match(r"^\d[\d.]*,\d+$", c):
                n += 1
    return n, title


for yr in [1990, 1995, 1998, 2000, 2001, 2002]:
    for name, url in [
        ("historica", f"https://www.bcp.gov.py/webapps/web/cotizacion/monedas-historica?anho={yr}&moneda=USD"),
        ("fluctuante", f"https://www.bcp.gov.py/webapps/web/cotizacion/referencial-fluctuante/anual?anho={yr}&tipoOperacion=compra"),
        ("mensual", f"https://www.bcp.gov.py/webapps/web/cotizacion/monedas-mensual?anho={yr}&mes=1"),
    ]:
        code, html = fetch(url)
        n, title = grid_has_data(html)
        print(f"{name} {yr}: HTTP {code} datacells={n} title={title!r}")
