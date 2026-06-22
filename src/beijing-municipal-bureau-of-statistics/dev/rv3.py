import subsets_utils as su, re
H="https://hgk.tjj.beijing.gov.cn"
v=H+"/query/queryReport/queryReportAction?method=queryHtmlStyle&queryCondition.reportNumber=60Y-1-03-N&queryCondition.objectType=04&queryCondition.objectCode=0100&yhid=guest&netType=2"
h=su.get(v,timeout=(10,60)).text
i=h.find('reportVersion=201301')
print(repr(h[i-120:i+260]))
