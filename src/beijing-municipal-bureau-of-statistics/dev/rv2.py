import subsets_utils as su, re
H="https://hgk.tjj.beijing.gov.cn"
v=H+"/query/queryReport/queryReportAction?method=queryHtmlStyle&queryCondition.reportNumber=60Y-1-03-N&queryCondition.objectType=04&queryCondition.objectCode=0100&yhid=guest&netType=2"
h=su.get(v,timeout=(10,60)).text
for m in re.finditer(r'.{40}reportVersion.{40}', h):
    print(repr(m.group(0)))
