import io, httpx, pandas as pd
# private client, verify disabled — daff.gov.au has an expired/broken cert
c = httpx.Client(verify=False, follow_redirects=True, timeout=httpx.Timeout(15,read=180),
                 headers={"User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/120 Safari/537.36"})
import warnings; warnings.filterwarnings("ignore")
cases = {
 "link_xls (agcom, redirect->daff)": "https://data.gov.au/data/dataset/b84c3235-e370-47dc-831e-cdb989c3f3a4/resource/155f4c32-3a4e-4c8f-b0da-cdfee879f3a0/download/AgCommodities201412_Tables_1.0.0.xls",
 "link_xlsx (awmr, redirect->daff)": "https://data.gov.au/data/dataset/05036866-1383-40a1-855e-a29adfc9c121/resource/20f64fa1-ef2a-4a82-ba65-da123a52109a/download/awmr2015-16_chartsTables_v4.0.0.xlsx",
 "upload_csv (forests, data.gov.au)": "https://data.gov.au/data/dataset/c426860e-9b55-404e-9892-e975794018d5/resource/849a0d00-577a-4eb2-b77f-4d63264201ae/download/aus_for23_attributes.csv",
}
for name,u in cases.items():
    try:
        r=c.get(u); r.raise_for_status(); b=r.content
        if u.endswith(".csv"):
            df=pd.read_csv(io.BytesIO(b),dtype=str,header=None); sh={"_":df}
        else:
            sh=pd.read_excel(io.BytesIO(b),sheet_name=None,header=None,dtype=str)
        cells=sum(int(d.notna().sum().sum()) for d in sh.values())
        print(f"OK  {name:38s} bytes={len(b):>8} sheets={len(sh)} cells={cells}")
    except Exception as e:
        print(f"ERR {name:38s} {type(e).__name__}: {str(e)[:70]}")
