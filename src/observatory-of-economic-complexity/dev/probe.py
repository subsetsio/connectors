from subsets_utils import get
B="https://api.oec.world/tesseract/data.csv"

def q(params):
    r=get(B, params=params, timeout=(10,180))
    return r.status_code, len(r.content), r.text.splitlines()[:1]

# 1. comma-separated drilldowns via httpx params
print("ECI whole:", q({"cube":"complexity_eci_a_hs92_hs4","drilldowns":"Country Official,Year","measures":"ECI"})[:2])
# 2. 413 detection (BACI whole)
print("BACI22 whole:", q({"cube":"trade_i_baci_a_22","drilldowns":"HS6 Official,Exporter Country Official,Year","measures":"Trade Value,Quantity"})[:2])
# 3. BACI per-year
sc,sz,h=q({"cube":"trade_i_baci_a_22","drilldowns":"HS6 Official,Exporter Country Official,Year","measures":"Trade Value,Quantity","Year":"2022"})
print("BACI22 Year=2022:",sc,sz,h)
# 4. 13f whole size
sc,sz,h=q({"cube":"13f_managers","drilldowns":"Report Period Date,Central Key Index,Filing Manager Name","measures":"Market Value,Holdings"})
print("13f whole:",sc,sz,h)
# 5. comtrade_m_hs per month HS2
sc,sz,h=q({"cube":"trade_i_comtrade_m_hs","drilldowns":"Trade Flow,Reporter Country Official,HS2 Official,Time","measures":"Trade Value,Net Weight","Time":"202001"})
print("comtrade_m HS2 Time=202001:",sc,sz,h)
# 6. members endpoint
r=get("https://api.oec.world/tesseract/members", params={"cube":"trade_i_baci_a_22","level":"Year"}, timeout=(10,60))
print("members:", r.status_code, r.json().get("members"))
