"""Generate one tests/<spec_id>.yaml per download node, authored from belief.

Raw layer = NDJSON straight from the CBN GetAll* endpoints. read_json_auto types:
  - id            -> BIGINT  (integer)   primary key, present + unique
  - tyear/tmonth  -> BIGINT  (monthly datasets)   GDP's tyear is VARCHAR (quoted)
  - GetAllExchangeRates.ratedate -> DATE (ISO yyyy-mm-dd auto-detected)
  - everything else (dates as dd/mm/yyyy or Month-DD-YYYY, all numeric values) -> VARCHAR

Engine quirks honoured here:
  - between/at_most/at_least/freshness use raw min()/max(); on VARCHAR that is
    LEXICOGRAPHIC, so numeric range checks only go on BIGINT or 4-digit-year cols.
  - median_between/mean_between TRY_CAST to DOUBLE -> the safe value-unit guard
    for the string-typed numeric columns.
  - freshness max() is reliable only on the real DATE column (exchange rates).
"""
import os
import yaml

SLUG = "central-bank-of-nigeria"
TESTS_DIR = os.path.join(os.path.dirname(__file__), "..", "tests")
os.makedirs(TESTS_DIR, exist_ok=True)


def spec_id(entity):
    return f"{SLUG}-{entity.lower().replace('_', '-')}"


# id-key tests shared by every dataset (id is a BIGINT primary key everywhere).
def id_tests():
    return [
        {"not_null": "id", "certainty": 99,
         "reason": "id is the source primary key; every record carries one"},
        {"column_type": {"col": "id", "type": "integer"},
         "certainty": 95,
         "reason": "id arrives as a JSON number -> BIGINT"},
        {"unique": "id", "certainty": 90,
         "reason": "id is the source primary key; dupes mean the array was fetched/concatenated twice"},
    ]


DMY = r"^\d{2}/\d{2}/\d{4}$"        # 30/11/2023
ISO = r"^\d{4}-\d{2}-\d{2}$"        # 2026-06-22
MONTH_DMY = r"^[A-Za-z]+-\d{1,2}-\d{4}$"  # June-19-2026

# entity -> list of dataset-specific tests (id tests are prepended automatically)
DATASETS = {
    "GetAllAssetsLiabilities": [
        {"not_null": "payDate", "certainty": 99, "reason": "monthly balance-sheet date index"},
        {"column_type": {"col": "payDate", "type": "string"}, "certainty": 95,
         "reason": "raw keeps the dd/mm/yyyy string; casting to DATE is the transform's job"},
        {"matches": {"col": "payDate", "pattern": DMY}, "certainty": 90,
         "reason": "source emits dd/mm/yyyy"},
        {"not_null": "period", "certainty": 90},
        {"column_type": {"col": "totalAss", "type": "string"}, "certainty": 90,
         "reason": "numeric values come back as quoted strings"},
        {"median_between": {"col": "totalAss", "lo": 1e6, "hi": 1e13}, "certainty": 45,
         "severity": "warn", "reason": "central-bank total assets are large positive Naira-thousands; unit guard"},
        {"row_count": {"min": 150}, "certainty": 85,
         "reason": "monthly since 2005 (~229 now), grows one row/month; a sharp drop = partial pull"},
    ],
    "GetAllCrudeOilPrices": [
        {"not_null": "period", "certainty": 95},
        {"column_type": {"col": "tyear", "type": "integer"}, "certainty": 95},
        {"column_type": {"col": "tmonth", "type": "integer"}, "certainty": 95},
        {"at_least": {"col": "tyear", "expr": 2000}, "certainty": 90,
         "reason": "series begins in the 2000s"},
        {"at_most": {"col": "tyear", "expr": "current_year()"}, "certainty": 75,
         "severity": "warn", "points_outward": True,
         "reason": "no future years expected; a breach means the source published ahead"},
        {"column_type": {"col": "crudeOilPrice", "type": "string"}, "certainty": 90},
        {"median_between": {"col": "crudeOilPrice", "lo": 20, "hi": 200}, "certainty": 60,
         "severity": "warn", "reason": "USD/barrel; median should sit in the tens-to-low-hundreds"},
        {"row_count": {"min": 150}, "certainty": 85},
    ],
    "GetAllDailyCrude": [
        {"not_null": "postDate", "certainty": 99, "reason": "daily price date index"},
        {"column_type": {"col": "postDate", "type": "string"}, "certainty": 95},
        {"matches": {"col": "postDate", "pattern": DMY}, "certainty": 90},
        {"column_type": {"col": "crudeOilPrice", "type": "string"}, "certainty": 90},
        {"median_between": {"col": "crudeOilPrice", "lo": 20, "hi": 200}, "certainty": 60,
         "severity": "warn", "reason": "USD/barrel spot price"},
        {"row_count": {"min": 2500}, "certainty": 85,
         "reason": "daily since 2009 (~3.9k now); grows ~250/yr"},
    ],
    "GetAllDiscountRates": [
        {"not_null": "ratedate", "certainty": 99},
        {"column_type": {"col": "ratedate", "type": "string"}, "certainty": 95},
        {"matches": {"col": "ratedate", "pattern": DMY}, "certainty": 90},
        {"not_null": "ratetype", "certainty": 90, "reason": "each rate row names its instrument"},
        {"distinct_count": {"col": "ratetype", "min": 2}, "certainty": 80, "severity": "warn",
         "reason": "several rate types (MPR, reverse rate, ...)"},
        {"median_between": {"col": "amount", "lo": 1, "hi": 40}, "certainty": 50, "severity": "warn",
         "reason": "policy/discount rates are single-to-low-double-digit percent"},
        {"row_count": {"min": 3500}, "certainty": 85},
    ],
    "GetAllExchangeRates": [
        {"not_null": "ratedate", "certainty": 99},
        {"column_type": {"col": "ratedate", "type": "date"}, "certainty": 85,
         "reason": "ISO yyyy-mm-dd strings are auto-detected as DATE by read_json_auto"},
        {"matches": {"col": "ratedate", "pattern": ISO}, "certainty": 90,
         "reason": "source emits ISO dates; cast-to-varchar stays yyyy-mm-dd"},
        {"not_null": "currency", "certainty": 95},
        {"distinct_count": {"col": "currency", "min": 5}, "certainty": 85, "severity": "warn",
         "reason": "multiple quoted currencies (USD, GBP, EUR, YEN, CFA, ...)"},
        {"column_type": {"col": "sellingrate", "type": "string"}, "certainty": 90},
        {"freshness": {"col": "ratedate", "reaches": "today - 21d"}, "certainty": 70,
         "severity": "warn", "points_outward": True,
         "reason": "FX is published most business days; a stale max usually means source lag"},
        {"row_count": {"min": 40000}, "certainty": 85,
         "reason": "per-currency daily since 2001 (~61k now)"},
    ],
    "GetAllFinancialData": [
        {"not_null": "recDate", "certainty": 99},
        {"column_type": {"col": "recDate", "type": "string"}, "certainty": 95},
        {"matches": {"col": "recDate", "pattern": DMY}, "certainty": 90},
        {"column_type": {"col": "opeBal", "type": "string"}, "certainty": 90},
        {"row_count": {"min": 2500}, "certainty": 85,
         "reason": "daily money-market flows since 2009 (~3.6k now)"},
    ],
    "GetAllFiveYearStatement": [
        {"not_null": "year", "certainty": 99, "reason": "annual statement year"},
        {"column_type": {"col": "year", "type": "string"}, "certainty": 90,
         "reason": "year is a quoted 4-digit string in the raw"},
        {"matches": {"col": "year", "pattern": r"^\d{4}$"}, "certainty": 90},
        {"between": {"col": "year", "lo": 1958, "hi": "current_year()"}, "certainty": 80,
         "severity": "warn",
         "reason": "annual CBN statement years; 4-digit strings order the same lexically and numerically"},
        {"not_null": "date", "certainty": 95},
        {"matches": {"col": "date", "pattern": r"^\d{1,2} [A-Za-z]+, \d{4}$"}, "certainty": 80,
         "severity": "warn", "reason": "free-text 'DD Month, YYYY' date label"},
        {"row_count": {"min": 25}, "certainty": 80,
         "reason": "one row/year of audited statements (~41 now)"},
    ],
    "GetAllInflationRates": [
        {"not_null": "period", "certainty": 95},
        {"column_type": {"col": "tyear", "type": "integer"}, "certainty": 95},
        {"column_type": {"col": "tmonth", "type": "integer"}, "certainty": 95},
        {"at_least": {"col": "tyear", "expr": 2000}, "certainty": 90},
        {"at_most": {"col": "tyear", "expr": "current_year()"}, "certainty": 75,
         "severity": "warn", "points_outward": True},
        {"median_between": {"col": "allItemsYearOn", "lo": 2, "hi": 60}, "certainty": 55,
         "severity": "warn", "reason": "Nigeria headline YoY CPI inflation, percent"},
        {"row_count": {"min": 180}, "certainty": 85,
         "reason": "monthly since 2003 (~281 now)"},
    ],
    "GetAllIntPayments": [
        {"not_null": "payDate", "certainty": 99},
        {"column_type": {"col": "payDate", "type": "string"}, "certainty": 95},
        {"matches": {"col": "payDate", "pattern": DMY}, "certainty": 90},
        {"column_type": {"col": "total", "type": "string"}, "certainty": 90},
        {"row_count": {"min": 250}, "certainty": 85,
         "reason": "monthly interest/payment records since 2003 (~376 now)"},
    ],
    "GetAllInterbankRates": [
        {"not_null": "ratedate", "certainty": 99},
        {"column_type": {"col": "ratedate", "type": "string"}, "certainty": 95,
         "reason": "Month-DD-YYYY string; casting is the transform's job"},
        {"matches": {"col": "ratedate", "pattern": MONTH_DMY}, "certainty": 85,
         "reason": "source emits 'June-19-2026' style dates"},
        {"not_null": "ratetype", "certainty": 90},
        {"median_between": {"col": "weightedaverage", "lo": 1, "hi": 60}, "certainty": 50,
         "severity": "warn", "reason": "interbank rates in percent"},
        {"row_count": {"min": 10000}, "certainty": 85,
         "reason": "daily per-tenor since 2001 (~18k now)"},
    ],
    "GetAllMoneyAndCreditStats": [
        {"not_null": "period", "certainty": 95},
        {"column_type": {"col": "tyear", "type": "integer"}, "certainty": 95},
        {"at_least": {"col": "tyear", "expr": 1955}, "certainty": 90,
         "reason": "monetary aggregates reach back to ~1960"},
        {"at_most": {"col": "tyear", "expr": "current_year()"}, "certainty": 75,
         "severity": "warn", "points_outward": True},
        {"median_between": {"col": "moneySupply_M2", "lo": 100, "hi": 1e9}, "certainty": 40,
         "severity": "warn", "reason": "broad money in Naira-millions; wide positive unit guard"},
        {"row_count": {"min": 300}, "certainty": 85,
         "reason": "monthly+early-annual since 1960 (~433 now)"},
    ],
    "GetAllMoneyMarketIndicators": [
        {"not_null": "period", "certainty": 95},
        {"column_type": {"col": "tyear", "type": "integer"}, "certainty": 95},
        {"at_least": {"col": "tyear", "expr": 2000}, "certainty": 90},
        {"at_most": {"col": "tyear", "expr": "current_year()"}, "certainty": 75,
         "severity": "warn", "points_outward": True},
        {"median_between": {"col": "mpr", "lo": 5, "hi": 30}, "certainty": 50, "severity": "warn",
         "reason": "monetary policy rate, percent"},
        {"row_count": {"min": 150}, "certainty": 85,
         "reason": "monthly since 2006 (~245 now)"},
    ],
    "GetAllMonthlyAvgExchRates": [
        {"not_null": "period", "certainty": 95},
        {"column_type": {"col": "tyear", "type": "integer"}, "certainty": 95},
        {"at_least": {"col": "tyear", "expr": 2000}, "certainty": 90},
        {"at_most": {"col": "tyear", "expr": "current_year()"}, "certainty": 75,
         "severity": "warn", "points_outward": True},
        {"column_type": {"col": "ifemDollar", "type": "string"}, "certainty": 90},
        {"row_count": {"min": 120}, "certainty": 85,
         "reason": "monthly average FX since 2004 (~208 now)"},
    ],
    "GetAllNominalGDP": [
        {"not_null": "period", "certainty": 95, "reason": "Q1..Q4 / Annual marker"},
        {"enum": {"col": "period", "values": ["Q1", "Q2", "Q3", "Q4", "Annual"]},
         "certainty": 70, "severity": "warn",
         "reason": "GDP rows are quarterly or full-year"},
        {"column_type": {"col": "tyear", "type": "string"}, "certainty": 85,
         "reason": "GDP tyear is a quoted 4-digit string in the raw"},
        {"between": {"col": "tyear", "lo": 1980, "hi": "current_year()"}, "certainty": 80,
         "severity": "warn", "reason": "4-digit years order identically lexically and numerically"},
        {"column_type": {"col": "gdPatCurrentMarketPrices", "type": "string"}, "certainty": 90},
        {"row_count": {"min": 60}, "certainty": 80,
         "reason": "annual+quarterly since 1981 (~104 now)"},
    ],
    "GetAllRealGDP": [
        {"not_null": "period", "certainty": 95},
        {"enum": {"col": "period", "values": ["Q1", "Q2", "Q3", "Q4", "Annual"]},
         "certainty": 70, "severity": "warn"},
        {"column_type": {"col": "tyear", "type": "string"}, "certainty": 85},
        {"between": {"col": "tyear", "lo": 1980, "hi": "current_year()"}, "certainty": 80,
         "severity": "warn"},
        {"column_type": {"col": "gdPatCurrentMarketPrices", "type": "string"}, "certainty": 90},
        {"row_count": {"min": 60}, "certainty": 80},
    ],
    "GetAllReserves": [
        {"not_null": "moveDate", "certainty": 99},
        {"column_type": {"col": "moveDate", "type": "string"}, "certainty": 95},
        {"matches": {"col": "moveDate", "pattern": DMY}, "certainty": 90},
        {"column_type": {"col": "gross", "type": "string"}, "certainty": 90},
        {"median_between": {"col": "gross", "lo": 1e9, "hi": 1e12}, "certainty": 55, "severity": "warn",
         "reason": "external reserves in USD, tens of billions"},
        {"row_count": {"min": 3000}, "certainty": 85,
         "reason": "daily reserves since 2006 (~4.9k now)"},
    ],
}

# The five securities datasets share one auction-level schema.
def securities_tests(row_min, certainty_rc):
    return [
        {"not_null": "auctionDate", "certainty": 99, "reason": "auction date index"},
        {"column_type": {"col": "auctionDate", "type": "string"}, "certainty": 95},
        {"matches": {"col": "auctionDate", "pattern": MONTH_DMY}, "certainty": 85,
         "reason": "source emits 'June-22-2026' style auction dates"},
        {"not_null": "securityType", "certainty": 90},
        {"column_type": {"col": "rate", "type": "string"}, "certainty": 90},
        {"row_count": {"min": row_min}, "certainty": certainty_rc},
    ]


DATASETS["GetAllSecurities"] = securities_tests(3000, 85)        # ~4.7k
DATASETS["GetAllSecuritiesCBNBill"] = securities_tests(3, 60)    # only ~10 (rare instrument)
DATASETS["GetAllSecuritiesFGNBond"] = securities_tests(300, 85)  # ~508
DATASETS["GetAllSecuritiesNTB"] = securities_tests(1000, 85)     # ~1.8k
DATASETS["GetAllSecuritiesOMO"] = securities_tests(1500, 85)     # ~2.4k

# CBNBill is a tiny, rarely-updated slice — soften its row-count to a warn.
for t in DATASETS["GetAllSecuritiesCBNBill"]:
    if "row_count" in t:
        t["severity"] = "warn"
        t["reason"] = "CBN Certificate is a sparse, mostly-historical instrument (~10 rows)"


for entity, extra in DATASETS.items():
    sid = spec_id(entity)
    doc = {
        "spec_id": sid,
        "status": "active",
        "tests": id_tests() + extra,
    }
    path = os.path.join(TESTS_DIR, f"{sid}.yaml")
    with open(path, "w") as f:
        f.write(f"# Expectations for {entity} (CBN GetAll* raw, NDJSON).\n")
        yaml.safe_dump(doc, f, sort_keys=False, default_flow_style=False, width=100)
    print("wrote", os.path.relpath(path))

print(f"\n{len(DATASETS)} test specs written")
