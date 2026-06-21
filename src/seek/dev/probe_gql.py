from subsets_utils import post
EP="https://ap-southeast-2-seek-apac.cdn.hygraph.com/content/cl583oqu74ttw01ug0g4s5hmt/master"
Q='{ assets(where: {mimeType: "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"}, orderBy: updatedAt_DESC, first: 100) { fileName url updatedAt } }'
# note: deliberately malformed brace above? no—fix:
Q='{ assets(where: {mimeType: "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"}, orderBy: updatedAt_DESC, first: 100) { fileName url updatedAt } }'
r = post(EP, json={"query": Q}, timeout=(10,60))
r.raise_for_status()
data = r.json()["data"]["assets"]
print("total xlsx assets:", len(data))
def pick(pred):
    cand = [a for a in data if pred(a["fileName"])]
    cand.sort(key=lambda a: a["updatedAt"], reverse=True)
    return cand[0] if cand else None
emp = pick(lambda f: f.startswith("AU_PUBLISHED_DATASET"))
sal = pick(lambda f: f.startswith("seek_asi_") and not f.lower().startswith("seek_asi_nz"))
print("EMP ->", emp)
print("SAL ->", sal)
