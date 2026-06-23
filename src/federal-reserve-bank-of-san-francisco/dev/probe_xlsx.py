import io, pandas as pd
from subsets_utils import get

FILES = {
 "news_sentiment": "https://www.frbsf.org/wp-content/uploads/news_sentiment_data.xlsx",
 "tfp": "https://www.frbsf.org/wp-content/uploads/quarterly_tfp.xlsx",
 "cpi_contrib": "https://www.frbsf.org/wp-content/uploads/cpi-contributors-data.xlsx",
 "regional": "https://www.frbsf.org/wp-content/uploads/regional-indicators-data.xlsx",
 "usmpd": "https://www.frbsf.org/wp-content/uploads/USMPD.xlsx",
 "proxy": "https://www.frbsf.org/wp-content/uploads/proxy-funds-rate-data.xlsx",
 "term_model": "https://www.frbsf.org/wp-content/uploads/FRBSF_Term_Model_Data.xlsx",
 "excess_savings": "https://www.frbsf.org/wp-content/uploads/excess_savings_data.xlsx",
}
for name,url in FILES.items():
    print("\n"+"="*70)
    print(name, url.split("/")[-1])
    try:
        r = get(url, timeout=(10,90)); r.raise_for_status()
        xl = pd.ExcelFile(io.BytesIO(r.content))
        print("  sheets:", xl.sheet_names)
        for sh in xl.sheet_names[:4]:
            df = xl.parse(sh, header=None, nrows=8)
            print(f"  --- sheet '{sh}'  shape(first8 x {df.shape[1]}cols)")
            for i,row in df.iterrows():
                vals=[str(v)[:18] for v in row.tolist()[:8]]
                print("     r%d:"%i, " | ".join(vals))
    except Exception as e:
        print("  ERROR", type(e).__name__, e)
