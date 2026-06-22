import httpx,warnings; warnings.filterwarnings("ignore")
c=httpx.Client(verify=False,follow_redirects=True,timeout=25,headers={"User-Agent":"Mozilla/5.0"})
for i in range(3):
    try:
        r=c.get("https://data.daff.gov.au/data/warehouse/9aaw/2017/awmr_d9aawr20171129/awmr2015-16_chartsTables_v4.0.0.xlsx"); print(f"  try{i} status={r.status_code} size={len(r.content)}")
    except Exception as e: print(f"  try{i} ERR {type(e).__name__}: {str(e)[:50]}")
