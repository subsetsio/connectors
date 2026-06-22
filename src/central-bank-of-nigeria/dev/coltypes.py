import json, os
import duckdb
from subsets_utils import get

ENTITIES = [
    "GetAllAssetsLiabilities", "GetAllCrudeOilPrices", "GetAllDailyCrude",
    "GetAllDiscountRates", "GetAllExchangeRates", "GetAllFinancialData",
    "GetAllFiveYearStatement", "GetAllInflationRates", "GetAllIntPayments",
    "GetAllInterbankRates", "GetAllMoneyAndCreditStats", "GetAllMoneyMarketIndicators",
    "GetAllMonthlyAvgExchRates", "GetAllNominalGDP", "GetAllRealGDP", "GetAllReserves",
    "GetAllSecurities", "GetAllSecuritiesCBNBill", "GetAllSecuritiesFGNBond",
    "GetAllSecuritiesNTB", "GetAllSecuritiesOMO",
]
os.makedirs("dev/tmp", exist_ok=True)
con = duckdb.connect()
for e in ENTITIES:
    r = get("https://www.cbn.gov.ng/api/" + e, params={"format": "json"}, timeout=(10.0, 120.0))
    r.raise_for_status()
    data = r.json()
    p = f"dev/tmp/{e}.ndjson"
    with open(p, "w") as f:
        for row in data:
            f.write(json.dumps(row) + "\n")
    cols = con.execute(
        f"SELECT column_name, column_type FROM (DESCRIBE SELECT * FROM read_json_auto('{p}'))"
    ).fetchall()
    print(f"\n### {e}  n={len(data)}")
    for name, typ in cols:
        print(f"    {name}: {typ}")
