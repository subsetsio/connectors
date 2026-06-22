import re
from subsets_utils import post

ENDPOINT_MON = "https://cotizaciones.bcu.gub.uy/wscotizaciones/servlet/awsbcumonedas"
ENDPOINT_COT = "https://cotizaciones.bcu.gub.uy/wscotizaciones/servlet/awsbcucotizaciones"
HEADERS = {"Content-Type": "text/xml; charset=utf-8", "SOAPAction": "Cotiza"}


def monedas(grupo):
    env = (
        '<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" '
        'xmlns:cot="Cotiza"><soapenv:Body>'
        f"<cot:wsbcumonedas.Execute><cot:Entrada><cot:Grupo>{grupo}</cot:Grupo>"
        "</cot:Entrada></cot:wsbcumonedas.Execute></soapenv:Body></soapenv:Envelope>"
    )
    r = post(ENDPOINT_MON, data=env.encode(), headers=HEADERS, timeout=(10, 120), verify=False)
    return r.text


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
    r = post(ENDPOINT_COT, data=env.encode(), headers=HEADERS, timeout=(10, 300), verify=False)
    return r.text


for g in (0, 1, 2):
    t = monedas(g)
    codes = re.findall(r"<Codigo>\s*(\d+)\s*</Codigo>", t)
    print(f"grupo {g}: {len(codes)} currencies; sample {codes[:6]}")

print("\n=== USD billete (2225) full-history probe, grupo 2, 1980-2026 ===")
t = cotiz(2225, 2, "1980-01-01", "2026-06-22")
# show one full <dato> block to see all fields
m = re.search(r"<datoscotizaciones\.dato>.*?</datoscotizaciones\.dato>", t, re.S)
print("first dato block:\n", m.group(0) if m else "NO DATA")
print("status:", re.search(r"<status>(-?\d+)</status>", t).group(1) if re.search(r"<status>(-?\d+)</status>", t) else "?")
print("mensaje:", re.search(r"<mensaje>([^<]*)</mensaje>", t).group(1) if re.search(r"<mensaje>([^<]*)</mensaje>", t) else "")
fechas = re.findall(r"<Fecha>([^<]+)</Fecha>", t)
print("num rows:", len(fechas), "| earliest:", min(fechas) if fechas else None, "| latest:", max(fechas) if fechas else None)
