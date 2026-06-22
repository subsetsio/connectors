from subsets_utils import post
ns="http://www.banguat.gob.gt/variables/ws/"
ep="http://www.banguat.gob.gt/variables/ws/TipoCambio.asmx"
body=f'<?xml version="1.0" encoding="utf-8"?><soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"><soap:Body><TipoCambioDia xmlns="{ns}"/></soap:Body></soap:Envelope>'
try:
    r=post(ep,data=body,headers={"Content-Type":"text/xml; charset=utf-8","SOAPAction":f'"{ns}TipoCambioDia"'},timeout=(10,40))
    print("HTTP",r.status_code)
    print(r.text[:800])
except Exception as e:
    print("ERR",type(e).__name__,str(e)[:200])
