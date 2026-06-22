import sys; sys.path.insert(0, "src")
from subsets_utils import get
DS="23e0cdd56bddb4ad3016a9c3ad63a539"; DOM=29
for ps in (100,50,25,10,5):
    for page in (1,2):
        try:
            r=get(f"https://bpstat.bportugal.pt/data/v1/domains/{DOM}/datasets/{DS}/",
                  params={"lang":"EN","page":page,"page_size":ps}, timeout=(10,180))
            body=r.text
            ct=r.headers.get("content-type")
            print(f"ps={ps} page={page} status={r.status_code} ct={ct} len={len(body)} head={body[:120]!r}")
        except Exception as e:
            print(f"ps={ps} page={page} ERROR {type(e).__name__}: {e}")
