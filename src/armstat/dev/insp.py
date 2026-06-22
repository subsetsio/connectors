import sys,json
sys.path.insert(0,"src")
import nodes.armstat as m
base=m.HOST+m.ASSET_PATHS["armstat-tt-tr-fa4"]
page=m._get(base).text
form={**m._hidden_fields(page), m._VIEW_BTN:"View table","__EVENTTARGET":"","__EVENTARGUMENT":""}
form.update(m._listbox_selection(page))
m._post(base,form)
ds=m._get(base+"table/tableViewLayout1/?downloadfile=FileTypeJsonStat2").json()
print("id:",ds.get("id"))
for d in ds.get("id",[]):
    dim=ds["dimension"][d]
    print(" dim code=%r label=%r"%(d, dim.get("label")))
