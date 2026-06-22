import subsets_utils as su, re
H="https://hgk.tjj.beijing.gov.cn"
for rpt,subj,sort,want in [("60Y-1-03-N","0100","01","201301"),("DBW-A01","1100","05","201101")]:
    v=H+f"/query/queryReport/queryReportAction?method=queryHtmlStyle&queryCondition.reportNumber={rpt}&queryCondition.objectType=04&queryCondition.objectCode={subj}&yhid=guest&netType=2&queryCondition.dataSortTypeCode={sort}"
    h=su.get(v,timeout=(10,60)).text
    print("==",rpt,"want",want,"present?",want in h)
    # find reportVersion assignments
    for m in sorted(set(re.findall(r'[rR]eportVersion[\"\'\s:=]+([0-9]{6})', h))): print('  reportVersion candidate:',m)
    for m in sorted(set(re.findall(r'(?:var\s+)?\w*[vV]ersion\w*\s*=\s*[\"\']?([0-9]{6})', h)))[:8]: print('  version=',m)
