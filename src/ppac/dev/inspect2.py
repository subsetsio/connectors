import io, re, json
from subsets_utils import get, post
import openpyxl
# 1) international crude raw titles
r=post("https://ppac.gov.in/AjaxController/getInternationalPricesCrudeOil",
       data={"financialYear":"2025-2026","reportBy":"4","pageId":"30"},
       headers={"X-Requested-With":"XMLHttpRequest"})
res=json.loads(r.text)["result"]
rows=list(res.values()) if isinstance(res,dict) else res
print("INTL CRUDE rows:",len(rows))
for row in rows:
    t=re.sub('<[^>]+>','',str(row.get('title',''))).strip()
    print("  title=",repr(t),"colspan=",repr(row.get('colspan')),"apr=",row.get('april'),"may=",row.get('may'))
# 2) snapshot date cell with read_only False vs True
h=get("https://ppac.gov.in/consumption/active-domestic-customers").text
u=re.findall(r'https://ppac\.gov\.in/uploads/[^"\']+\.xlsx',h)[0]
b=get(u).content
for ro in (False,True):
    wb=openpyxl.load_workbook(io.BytesIO(b),data_only=True,read_only=ro)
    rs=[list(x) for x in wb.worksheets[0].iter_rows(values_only=True)]
    print(f"read_only={ro} r3=",rs[3][:3])
