import base64, json
from subsets_utils import get, post

HOST = "https://wabi-south-africa-north-a-primary-api.analysis.windows.net"
TOKEN = "eyJrIjoiZTQ3Njg5MDktNGNjMS00MTY0LWE1M2EtNGE1Y2FiMTlhZDc2IiwidCI6IjkzYWVkYmRjLWNjNjctNDY1Mi1hYTEyLWQyNTBhODc2YWU3OSIsImMiOjh9"

tok = json.loads(base64.b64decode(TOKEN + "==").decode())
rk = tok["k"]
print("resourceKey", rk, "tenant", tok["t"], "cluster", tok["c"])
H = {"X-PowerBI-ResourceKey": rk}

# 1. modelsAndExploration
url = f"{HOST}/public/reports/{rk}/modelsAndExploration?preferReadOnlySession=true"
r = get(url, headers=H, timeout=(10,60))
print("modelsAndExploration", r.status_code)
me = r.json()
print("top keys:", list(me.keys()))
models = me.get("models", [])
print("n models", len(models))
if models:
    m = models[0]
    print("model keys", list(m.keys()))
    print("modelId", m.get("id"), "dbName", m.get("dbName"))
expl = me.get("exploration", {})
print("exploration keys", list(expl.keys()))
secs = expl.get("sections", [])
print("n sections", len(secs))
if secs:
    s0 = secs[0]
    print("section keys", list(s0.keys()))
    vcs = s0.get("visualContainers", [])
    print("n visualContainers", len(vcs))
    # find one with a query
    for vc in vcs:
        cfg = json.loads(vc.get("config","{}"))
        sv = cfg.get("singleVisual", {})
        pq = sv.get("prototypeQuery")
        if pq:
            print("=== sample visual type:", sv.get("visualType"))
            print(json.dumps(pq, indent=1)[:1500])
            break
