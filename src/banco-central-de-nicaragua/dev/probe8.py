from subsets_utils import get
BASE="https://www.bcn.gob.ni/sites/default/files/estadisticas/siec/datos/"
r=get(BASE+"1.1.xls", timeout=(10,60))
print("ctype",r.headers.get("content-type"),"len",len(r.content))
h=r.content.decode("iso-8859-1","replace")
print(repr(h[:600]))
print("....")
import re
print("has <table",h.lower().count("<table"),"has <tr",h.lower().count("<tr"),"<x:",h.count("<x:"),"spreadsheet", "Workbook" in h or "urn:schemas-microsoft" in h)
