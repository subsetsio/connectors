import subsets_utils as su, re
B = "https://hgk.tjj.beijing.gov.cn/ww/"
r = su.get(B+"MenuItemAction!queryMenu", timeout=(10,30))
html=r.text
# find action references and hrefs
acts = sorted(set(re.findall(r'[\w/]*\w+Action![\w]+', html)))
print("Actions in menu:", acts)
hrefs = sorted(set(re.findall(r'(?:href|src|url|action)\s*[=:]\s*["\']([^"\']+)["\']', html)))
print("\nLinks:")
for h in hrefs:
    if 'Action' in h or 'query' in h.lower() or 'report' in h.lower() or 'subject' in h.lower():
        print(" ", h)
# look for JS files
js = re.findall(r'src="([^"]+\.js)"', html)
print("\nJS:", js)
