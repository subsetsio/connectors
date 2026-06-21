from subsets_utils import configure_http, get
configure_http(headers={"User-Agent":"Mozilla/5.0 (compatible; subsets-bot/1.0)"})
KEY="579b464db66ec23bdd000001cdd3946e44ce4aad7209ff7b23ac571b"
import time
t=time.time()
r=get("https://api.data.gov.in/resource/067fea29-928e-493c-b576-df5154b3661a",
      params={"api-key":KEY,"format":"json","limit":100,"offset":0},timeout=(10,120))
d=r.json()
print("status",r.status_code,"count",len(d.get('records') or []),"total",d.get("total"),"in %.1fs"%(time.time()-t))
