import io
import pandas as pd
from subsets_utils import get

# (entity, primary file url) — the canonical xlsx for each, or csv where no xlsx
FILES = {
"china-cyclical-activity-tracker":"https://www.frbsf.org/wp-content/uploads/ccat_data.xlsx",
"cpi-inflation-contributions-from-goods-and-services":"https://www.frbsf.org/wp-content/uploads/cpi-contributors-data.xlsx",
"cyclical-and-acyclical-core-pce-inflation":"https://www.frbsf.org/wp-content/uploads/cyclical-acyclical-core-pce-data.xlsx",
"daily-news-sentiment-index":"https://www.frbsf.org/wp-content/uploads/news_sentiment_data.xlsx",
"interest-rate-probability-distributions":"https://www.frbsf.org/wp-content/uploads/interest-rate-probability-distributions-data.xlsx",
"labor-market-stress-indicator":"https://www.frbsf.org/wp-content/uploads/labor-market-stress-indicator-data.xlsx",
"market-based-monetary-policy-uncertainty":"https://www.frbsf.org/wp-content/uploads/market-based-monetary-policy-uncertainty-data.xlsx",
"monetary-policy-surprises":"https://www.frbsf.org/wp-content/uploads/monetary-policy-surprises-data.xlsx",
"pandemic-era-excess-savings":"https://www.frbsf.org/wp-content/uploads/excess_savings_data.xlsx",
"pce-inflation-contributions-from-goods-and-services":"https://www.frbsf.org/wp-content/uploads/pce-contributions-data.xlsx",
"pce-personal-consumption-expenditure-price-index-pcepi":"https://www.frbsf.org/wp-content/uploads/pce-releases.xlsx",
"proxy-funds-rate":"https://www.frbsf.org/wp-content/uploads/proxy-funds-rate-data.xlsx",
"regional-indicators-for-labor-markets-and-prices":"https://www.frbsf.org/wp-content/uploads/regional-indicators-data.xlsx",
"revisions-to-payroll-employment-gains":"https://www.frbsf.org/wp-content/uploads/revisions-to-payroll-employment-data.xlsx",
"supply-and-demand-driven-pce-inflation":"https://www.frbsf.org/wp-content/uploads/supply-demand-pce-inflation.xlsx",
"total-factor-productivity-tfp":"https://www.frbsf.org/wp-content/uploads/quarterly_tfp.xlsx",
"treasury-yield-premiums":"https://www.frbsf.org/wp-content/uploads/FRBSF_Term_Web_Chart_Data.xlsx",
"treasury-yield-skewness":"https://www.frbsf.org/wp-content/uploads/treasury-yield-skewness-data.xlsx",
"twelfth-district-business-sentiment":"https://www.frbsf.org/wp-content/uploads/twelfth-district-business-sentiment-data.xlsx",
"us-monetary-policy-event-study-database":"https://www.frbsf.org/wp-content/uploads/USMPD.xlsx",
"weather-adjusted-employment-change":"https://www.frbsf.org/wp-content/uploads/weather-adjustment-time-series.xlsx",
"zero-lower-bound-probabilities-at-different-time-horizons":"https://www.frbsf.org/wp-content/uploads/zero-lower-bound-probabilities-data.xlsx",
}

for eid, url in FILES.items():
    print("="*90)
    print(eid, "<-", url.rsplit("/",1)[-1])
    try:
        content = get(url, timeout=(10,120)).content
        xls = pd.ExcelFile(io.BytesIO(content))
        print("  sheets:", xls.sheet_names)
        for sn in xls.sheet_names[:4]:
            df = pd.read_excel(xls, sheet_name=sn, header=None, nrows=6)
            print(f"  --- sheet '{sn}' shape~(rows>=6,{df.shape[1]} cols), first 6 rows:")
            for i, row in df.iterrows():
                vals = [str(v)[:22] for v in row.tolist()[:8]]
                print(f"      r{i}: {vals}")
    except Exception as e:
        print("  ERROR", type(e).__name__, e)
