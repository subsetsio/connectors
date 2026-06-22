import subsets_utils as su, re
r = su.get("https://hgk.tjj.beijing.gov.cn/query/gotoWWdh.action?yhid=guest&subjectTypeCode=0", timeout=(10,30))
html=r.text
# find all hrefs and onclick targets
links = sorted(set(re.findall(r'href="([^"]+)"', html)))
for l in links:
    if l and not l.startswith('#') and '.css' not in l and '.js' not in l:
        print("HREF", l)
print("---onclick/js calls---")
for m in sorted(set(re.findall(r'(?:onclick|window\.open|location\.href)[^;\n]{0,120}', html)))[:30]:
    print(m)
