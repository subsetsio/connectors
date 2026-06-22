import re
from subsets_utils import post

ENDPOINT_COT = "https://cotizaciones.bcu.gub.uy/wscotizaciones/servlet/awsbcucotizaciones"
HEADERS = {"Content-Type": "text/xml; charset=utf-8", "SOAPAction": "Cotiza"}


def cotiz(code, grupo, desde, hasta):
    env = (
        '<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" '
        'xmlns:cot="Cotiza"><soapenv:Body>'
        "<cot:wsbcucotizaciones.Execute><cot:Entrada>"
        f"<cot:Moneda><cot:item>{code}</cot:item></cot:Moneda>"
        f"<cot:FechaDesde>{desde}</cot:FechaDesde><cot:FechaHasta>{hasta}</cot:FechaHasta>"
        f"<cot:Grupo>{grupo}</cot:Grupo>"
        "</cot:Entrada></cot:wsbcucotizaciones.Execute></soapenv:Body></soapenv:Envelope>"
    )
    r = post(ENDPOINT_COT, data=env.encode(), headers=HEADERS, timeout=(10, 300))
    return r.text


def info(t):
    st = re.search(r"<status>(-?\d+)</status>", t)
    msg = re.search(r"<mensaje>([^<]*)</mensaje>", t)
    fechas = re.findall(r"<Fecha>([^<]+)</Fecha>", t)
    return (st.group(1) if st else "?", msg.group(1) if msg else "",
            len(fechas), (min(fechas), max(fechas)) if fechas else None)


# find max window: try a few spans ending today
for span in ("2026-01-01", "2025-06-22", "2025-01-01", "2024-06-22", "2023-06-22"):
    t = cotiz(2225, 2, span, "2026-06-22")
    print(f"desde {span}: status/msg/n/range = {info(t)}")

print("\n=== full record block (1 year window) ===")
t = cotiz(2225, 2, "2025-06-22", "2026-06-22")
m = re.search(r"<datoscotizaciones\.dato>.*?</datoscotizaciones\.dato>", t, re.S)
print(m.group(0) if m else "NO DATA")

print("\n=== earliest data probe for USD 2225 grupo 2 (1-yr windows back in time) ===")
for y in ("2000", "1990", "1985", "1980"):
    t = cotiz(2225, 2, f"{y}-01-01", f"{y}-12-31")
    print(f"{y}: {info(t)}")
