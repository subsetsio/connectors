import subsets_utils as su, re, json, html
H="https://hgk.tjj.beijing.gov.cn"
NS=H+"/query/queryres/queryreport/QueryReportAction!"
def parse_viewer(rpt,subj,sort):
    v=H+f"/query/queryReport/queryReportAction?method=queryHtmlStyle&queryCondition.reportNumber={rpt}&queryCondition.objectType=04&queryCondition.objectCode={subj}&yhid=guest&netType=2&queryCondition.dataSortTypeCode={sort}"
    h=su.get(v,timeout=(10,60)).text
    m=re.search(r'id="showSinglereport"(.*?)></script>', h, re.S)
    seg=m.group(1)
    def g(k): 
        mm=re.search(k+r'\s*=\s*"?([^"\s>]+)"?', seg); return mm.group(1) if mm else None
    return {"reportVersion":g("reportVersion"),"dept":g("sourceDepartmentCode"),
            "freqType":g("collectFrequenceTypeCode"),"dataSortType":g("dataSortTypeCode")}

def parse_tpl(tpl):
    labels={}; datacells=[]
    for m in re.finditer(r'<td\s+id="td_(\d+)_(\d+)"(.*?)</td>', tpl, re.S):
        col=int(m.group(1)); row=int(m.group(2)); inner=m.group(3)
        dm=re.search(r'metaData\s*=\s*"([^"]+)"', inner)
        if dm: datacells.append((row,col,dm.group(1)))
        else:
            lm=re.search(r'<label[^>]*>(.*?)</label>', inner, re.S)
            if lm:
                txt=html.unescape(re.sub(r'<[^>]+>','',lm.group(1))).replace('\xa0',' ').strip()
                if txt: labels[(row,col)]=txt
    return labels, datacells

rpt,subj,sort="DBW-A01","1100","05"
info=parse_viewer(rpt,subj,sort); print("info",info)
fm=su.post(NS+"queryRptTimeFreqMask",data={"reportDataKeyDTO.reportNumber":rpt,"reportDataKeyDTO.usageType":"01","reportDataKeyDTO.dataSortTypeCode":sort},timeout=(10,60))
masks=json.loads(fm.text)[0]["list"]; print("n masks",len(masks),"first",masks[:3])
def datakey(mask):
    return {"reportDataKeyDTO.reportNumber":rpt,"reportDataKeyDTO.departmentCode":info["dept"],
     "reportDataKeyDTO.collectFrequenceMask":mask,"reportDataKeyDTO.collectDataVersion":"1",
     "reportDataKeyDTO.collectFrequenceTypeCode":info["freqType"],"reportDataKeyDTO.usageType":"01",
     "reportDataKeyDTO.objectType":"04","reportDataKeyDTO.objectCode":subj,
     "reportDataKeyDTO.reportVersion":info["reportVersion"]}
# template from mask0
tpl=su.post(NS+"updateReportHtml",data=datakey(masks[0]),timeout=(10,120)).text
labels,datacells=parse_tpl(tpl)
mincol=min(c for _,c,_ in datacells); minrow=min(r for r,_,_ in datacells)
def left(r): return " / ".join(labels[(r,c)] for c in range(mincol) if (r,c) in labels)
def top(c): return " / ".join(labels[(rr,c)] for rr in range(minrow) if (rr,c) in labels)
for mask in masks[:2]:
    rd=su.post(NS+"queryReportData",data=datakey(mask),timeout=(10,120)).text
    js=json.loads(rd)
    if not js: print("mask",mask,"EMPTY"); continue
    drow=js[0]["data"][0]; vmap=dict(zip(drow["metaData"],drow["value"]))
    trips=[(left(r),top(c),vmap.get(cid)) for r,c,cid in datacells if vmap.get(cid) not in (None,"")]
    print(f"mask {mask} DSID {js[0]['DSID']} triples {len(trips)}")
    for t in trips[:5]: print("   ",t)
