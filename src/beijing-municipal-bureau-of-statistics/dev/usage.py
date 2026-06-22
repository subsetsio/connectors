import subsets_utils as su, re, json
H="https://hgk.tjj.beijing.gov.cn"
NS=H+"/query/queryres/queryreport/QueryReportAction!"
for report,subject,sort in [("LS-1-07","3700","01"),("60Y-1-03-N","0100","01"),("LS-031-001","3700","01")]:
    v=H+f"/query/queryReport/queryReportAction?method=queryHtmlStyle&queryCondition.reportNumber={report}&queryCondition.objectType=04&queryCondition.objectCode={subject}&yhid=guest&netType=2&queryCondition.dataSortTypeCode={sort}"
    h=su.get(v,timeout=(10,60)).text
    m=re.search(r'id="showSinglereport"([^>]*)>',h); seg=m.group(1)
    ut=re.search(r'usageType\s*=\s*"?([^"\s>]*)"?',seg)
    rv=re.search(r'reportVersion\s*=\s*"?([^"\s>]*)"?',seg)
    print(report, "usageType=", ut.group(1) if ut else None, "reportVersion=", rv.group(1) if rv else None)
