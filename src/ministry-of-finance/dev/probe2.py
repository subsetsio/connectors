from subsets_utils import get
KEY="579b464db66ec23bdd000001cdd3946e44ce4aad7209ff7b23ac571b"
H={"User-Agent":"Mozilla/5.0 (compatible; subsets-bot/1.0)"}
rid="067fea29-928e-493c-b576-df5154b3661a"  # total 407
for lim in [10,100,500,1000]:
    r=get(f"https://api.data.gov.in/resource/{rid}",params={"api-key":KEY,"format":"json","limit":lim,"offset":0},headers=H,timeout=(10,120))
    d=r.json()
    print(f"limit={lim:>4} -> count={len(d.get('records') or [])} total={d.get('total')}")
# offset pagination
r=get(f"https://api.data.gov.in/resource/{rid}",params={"api-key":KEY,"format":"json","limit":100,"offset":400},headers=H,timeout=(10,120))
d=r.json()
print("offset=400 limit=100 -> count",len(d.get('records') or []),"first _2019 actual key present", 'sl_no_' in (d['records'][0] if d.get('records') else {}))
