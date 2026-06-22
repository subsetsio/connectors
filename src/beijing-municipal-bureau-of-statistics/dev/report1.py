import subsets_utils as su
H="https://hgk.tjj.beijing.gov.cn"
for report,subject,sort in [("1","0100","01"),("1","0100","05")]:
    v=H+f"/query/queryReport/queryReportAction?method=queryHtmlStyle&queryCondition.reportNumber={report}&queryCondition.objectType=04&queryCondition.objectCode={subject}&yhid=guest&netType=2&queryCondition.dataSortTypeCode={sort}"
    r=su.get(v,timeout=(10,60))
    print(f"report={report} sort={sort}: status {r.status_code} len {len(r.text)} showSingle? {'showSinglereport' in r.text}")
    print("   title/snippet:", r.text[:200].replace('\n',' ').replace('\r',' '))
