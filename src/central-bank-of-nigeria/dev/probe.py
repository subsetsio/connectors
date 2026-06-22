import json
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

for e in ENTITIES:
    url = "https://www.cbn.gov.ng/api/" + e
    try:
        r = get(url, params={"format": "json"}, timeout=(10.0, 120.0))
        r.raise_for_status()
        data = r.json()
    except Exception as ex:
        print(f"\n### {e}: ERROR {type(ex).__name__}: {ex}")
        continue
    if not isinstance(data, list):
        print(f"\n### {e}: non-list {type(data).__name__}")
        continue
    n = len(data)
    first = data[0] if n else {}
    last = data[-1] if n else {}
    print(f"\n### {e}  n={n}  keys={list(first.keys())}")
    print("  FIRST:", json.dumps(first)[:400])
    print("  LAST :", json.dumps(last)[:400])
