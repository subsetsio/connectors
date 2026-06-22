import subsets_utils as su, re
r = su.get("https://hgk.tjj.beijing.gov.cn/query/gotoWWdh.action?yhid=guest&subjectTypeCode=0", timeout=(10,30))
print("status", r.status_code, "len", len(r.text))
html=r.text
acts = sorted(set(re.findall(r'[\w/]*\w+Action![\w]+', html)))
print("Actions:", acts)
js = sorted(set(re.findall(r'src="([^"]+\.js)"', html)))
print("JS:", js)
# any queryres references
print("queryres refs:", sorted(set(re.findall(r'[\w./]*queryres[\w./!?=]*', html)))[:20])
print("\nHEAD:\n", html[:800])
