import sys, json
sys.path.insert(0,"src"); sys.path.insert(0,"src/nodes")
import beijing_municipal_bureau_of_statistics as M
from subsets_utils import get, post
HOST=M.HOST; VIEWER=M.VIEWER; ACTION=M.ACTION
m=json.load(open("dev/scan_merged.json"))
errs=[k for k,v in m.items() if isinstance(v,str)]
def raw_get_viewer(report,subject,sort):
    r=get(VIEWER,params={"method":"queryHtmlStyle","queryCondition.reportNumber":report,"queryCondition.objectType":"04","queryCondition.objectCode":subject,"queryCondition.dataSortTypeCode":sort,"yhid":"guest","netType":"2"},timeout=(10,60))
    return r
def raw_post(action,data):
    return post(ACTION+action,data=data,timeout=(10,60))
for sid in errs:
    ent=M._BY_SPEC[sid]; report,subject,sort=ent["report"],ent["subject"],ent["sort"]
    short=sid.split("statistics-")[1]
    try:
        vr=raw_get_viewer(report,subject,sort)
        v=M._parse_viewer(vr.text)
        if not v:
            print(f"{short}: viewer EMPTY (status {vr.status_code}) -> empty"); m[sid]=0; continue
        fm=raw_post("queryRptTimeFreqMask",{"reportDataKeyDTO.reportNumber":report,"reportDataKeyDTO.usageType":v["usageType"],"reportDataKeyDTO.dataSortTypeCode":sort})
        blocks=fm.json() or []
        masks=[]
        for b in blocks:
            if b.get("list"): masks+=b["list"]
            elif b.get("collectFrequenceMask"): masks.append(b["collectFrequenceMask"])
        if not masks:
            print(f"{short}: no masks -> empty"); m[sid]=0; continue
        dk=M._data_key(report,v["dept"],masks[0],v["freqType"],subject,v["reportVersion"],v["usageType"])
        dr=raw_post("queryReportData",dk)
        print(f"{short}: viewer ok, masks={masks[:3]}, dataStatus={dr.status_code} dataLen={len(dr.text)} body[:80]={dr.text[:80]!r}")
        m[sid]= ("ERR500" if dr.status_code>=500 else (0 if len(dr.text)<=3 else len(dr.text)))
    except Exception as e:
        print(f"{short}: EXC {type(e).__name__}: {str(e)[:100]}")
        m[sid]="ERR500"
json.dump(m,open("dev/scan_merged.json","w"),ensure_ascii=False)
print("saved")
