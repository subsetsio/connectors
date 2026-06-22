import subsets_utils as su, re
H="https://hgk.tjj.beijing.gov.cn"
for j in ["/query/queryreport/javascript/showSinglereport.js",
          "/query/queryreport/javascript/parseDataSet.js",
          "/query/queryreport/javascript/controlfill.js"]:
    r=su.get(H+j, timeout=(10,30))
    txt=r.text
    print("==== ",j, r.status_code, "len",len(txt))
    for m in sorted(set(re.findall(r'[\w./]*[Aa]ction![\w]+', txt))): print("  ACTION",m)
    for m in sorted(set(re.findall(r'url\s*[:=]\s*["\'][^"\']+["\']', txt)))[:30]: print("  URL",m)
