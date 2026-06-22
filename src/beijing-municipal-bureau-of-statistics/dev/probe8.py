import subsets_utils as su, re
H="https://hgk.tjj.beijing.gov.cn"
viewer = H+"/query/queryReport/queryReportAction?method=queryHtmlStyle&queryCondition.reportNumber=60Y-1-03-N&queryCondition.objectType=04&queryCondition.objectCode=0100&yhid=guest&netType=2"
r = su.get(viewer, timeout=(10,60))
html=r.text
js = sorted(set(re.findall(r'src="([^"]+\.js)"', html)))
print("JS files:")
for j in js: print(" ",j)
print("\nAction refs in viewer:")
for a in sorted(set(re.findall(r'[\w/]*\w+[Aa]ction[!?][\w=.]+', html))): print(" ",a)
print("\nmethod= refs:")
for a in sorted(set(re.findall(r'method=\w+', html))): print(" ",a)
print("\nqueryReportData/updateReportHtml/FreqMask refs:")
for a in sorted(set(re.findall(r'[\w./!?=]*(?:queryReportData|updateReportHtml|FreqMask|queryReportAction|TimeFreq)[\w./!?=]*', html)))[:40]: print(" ",a)
