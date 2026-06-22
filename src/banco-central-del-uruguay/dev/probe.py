import xml.etree.ElementTree as ET
from subsets_utils import post

COT="https://cotizaciones.bcu.gub.uy/wscotizaciones/servlet/awsbcucotizaciones"
MON="https://cotizaciones.bcu.gub.uy/wscotizaciones/servlet/awsbcumonedas"

def soap(url, action, inner):
    body=('<?xml version="1.0" encoding="utf-8"?>'
      '<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/" xmlns:cot="Cotiza">'
      f'<soap:Body>{inner}</soap:Body></soap:Envelope>').encode()
    r=post(url,data=body,headers={"Content-Type":"text/xml; charset=utf-8","SOAPAction":action},timeout=(10,120))
    r.raise_for_status()
    return ET.fromstring(r.content)

def monedas(grupo):
    root=soap(MON,"Cotizaaction/AWSBCUMONEDAS.Execute",
        f"<cot:wsbcumonedas.Execute><cot:Entrada><cot:Grupo>{grupo}</cot:Grupo></cot:Entrada></cot:wsbcumonedas.Execute>")
    out=[];code=None
    for el in root.iter():
        t=el.tag.rsplit("}",1)[-1]
        if t=="Codigo":code=int(el.text)
        elif t=="Nombre" and code is not None:out.append((code,(el.text or"").strip()));code=None
    return out

def cot(monedas_codes,desde,hasta,grupo):
    items="".join(f"<cot:item>{m}</cot:item>" for m in monedas_codes)
    inner=("<cot:wsbcucotizaciones.Execute><cot:Entrada>"
      f"<cot:Moneda>{items}</cot:Moneda>"
      f"<cot:FechaDesde>{desde}</cot:FechaDesde><cot:FechaHasta>{hasta}</cot:FechaHasta>"
      f"<cot:Grupo>{grupo}</cot:Grupo></cot:Entrada></cot:wsbcucotizaciones.Execute>")
    root=soap(COT,"Cotizaaction/AWSBCUCOTIZACIONES.Execute",inner)
    status=msg=None;rows=[];cur={}
    for el in root.iter():
        t=el.tag.rsplit("}",1)[-1]
        if t=="status":status=el.text
        elif t=="codigoerror":pass
        elif t=="mensaje":msg=el.text
        elif t in("Fecha","Moneda","Nombre","CodigoISO","Emisor","TCC","TCV","ArbAct","FormaArbitrar"):
            if t=="Fecha" and cur:rows.append(cur);cur={}
            cur[t]=el.text
    if cur and "Fecha" in cur:rows.append(cur)
    return status,msg,rows

g1=monedas(1)
codes=[c for c,_ in g1]
print("group1 codes:",len(codes))
s,m,rows=cot(codes,"2025-06-02","2025-06-06",1)
print("ALL CODES grp1 5d: status",s,"msg",repr(m),"rows",len(rows))
isos=sorted({r.get("CodigoISO") for r in rows})
print("  distinct ISO:",len(isos),isos)
print("  sample:",rows[0] if rows else None)
print("  uniq Forma:",sorted({r.get("FormaArbitrar") for r in rows}))
print("  emisor sample:",sorted({r.get("Emisor") for r in rows})[:10])

print("=== history depth probe (group 1, all codes) ===")
for yr in ["1990","1995","2000","2003","2005","2010"]:
    s,m,rows=cot(codes,f"{yr}-01-04",f"{yr}-01-31",1)
    print(yr,"-> status",s,"msg",repr(m),"rows",len(rows), "firstFecha", rows[0]['Fecha'] if rows else None)
