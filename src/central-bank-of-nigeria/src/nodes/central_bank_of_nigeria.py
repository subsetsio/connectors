"""Central Bank of Nigeria (cbn) connector.

Source: the CBN public JSON REST API at https://www.cbn.gov.ng/api/ that powers
the bank's "Data & Statistics" pages (/rates/*.html). Each dataset is exposed as
one `GetAll<Dataset>` endpoint returning the FULL time series as a single flat
JSON array (no pagination, no auth). Numeric values come back as JSON strings
(missing values as ""), so the transforms cast/clean.

Fetch shape: stateless full re-pull. Every endpoint returns the entire series in
one request (largest observed ~61k rows / a few MB), so we re-fetch the whole
corpus each run and overwrite — revisions and late corrections are picked up for
free. No incremental filter is offered by the source.
"""
import pyarrow as pa

from subsets_utils import (
    NodeSpec,
    SqlNodeSpec,
    get,
    save_raw_ndjson,
    transient_retry,
)

SLUG = "central-bank-of-nigeria"
PREFIX = SLUG + "-"
API_BASE = "https://www.cbn.gov.ng/api/"

# The rank-accepted entity union (original CamelCase endpoint names).
from constants import ENTITY_IDS


def _spec_id(entity_id: str) -> str:
    return PREFIX + entity_id.lower().replace("_", "-")


# Recover the original endpoint name from the (lower-cased) spec id the runtime
# hands the fetch fn. Built from the ENTITY_IDS constant — no I/O.
_ENTITY_BY_SPEC = {_spec_id(e): e for e in ENTITY_IDS}


# --------------------------------------------------------------------------- #
# Download                                                                     #
# --------------------------------------------------------------------------- #


@transient_retry()
def _fetch_json(url: str):
    # format=json is required on some endpoints (e.g. interbank) and harmless on
    # the rest. The host sits behind Cloudflare; subsets_utils.get sets a normal
    # browser-like User-Agent.
    resp = get(url, params={"format": "json"}, timeout=(10.0, 120.0))
    resp.raise_for_status()
    return resp.json()


def fetch_one(node_id: str) -> None:
    asset = node_id  # the spec id IS the asset name
    entity = _ENTITY_BY_SPEC[node_id]
    data = _fetch_json(API_BASE + entity)
    if not isinstance(data, list):
        raise TypeError(f"{entity}: expected JSON array, got {type(data).__name__}")
    # Drifty wide records with all-string numeric values -> NDJSON (no schema
    # burden; the SQL transform re-types on read).
    save_raw_ndjson(data, asset)


DOWNLOAD_SPECS = [
    NodeSpec(id=_spec_id(e), fn=fetch_one, kind="download") for e in ENTITY_IDS
]


# --------------------------------------------------------------------------- #
# Transform — one published Delta table per dataset                            #
# --------------------------------------------------------------------------- #

def _num(c: str) -> str:
    # Works whether the raw column is VARCHAR or numeric; "" -> NULL.
    return f"TRY_CAST(NULLIF(CAST(\"{c}\" AS VARCHAR), '') AS DOUBLE) AS \"{c}\""


def _txt(c: str) -> str:
    return f"NULLIF(CAST(\"{c}\" AS VARCHAR), '') AS \"{c}\""


def _dmy(c: str) -> str:  # dd/mm/yyyy
    return f"try_strptime(CAST(\"{c}\" AS VARCHAR), '%d/%m/%Y')::DATE"


def _mdy_long(c: str) -> str:  # Month-DD-YYYY  e.g. June-18-2026
    return f"try_strptime(CAST(\"{c}\" AS VARCHAR), '%B-%d-%Y')::DATE"


def _iso(c: str) -> str:  # yyyy-mm-dd
    return f"TRY_CAST(NULLIF(CAST(\"{c}\" AS VARCHAR), '') AS DATE)"


# Most monthly series also carry early *annual* rows where `tmonth` holds the
# year (period=' 1992') instead of 1..12. Build the month-start date for real
# months, fall back to year-end for the annual rows, and never feed make_date an
# out-of-range month (it raises rather than returning NULL).
_MONTHLY_DATE = (
    "CASE "
    "WHEN TRY_CAST(tmonth AS INTEGER) BETWEEN 1 AND 12 "
    "THEN make_date(TRY_CAST(tyear AS INTEGER), TRY_CAST(tmonth AS INTEGER), 1) "
    "WHEN TRY_CAST(tyear AS INTEGER) BETWEEN 1900 AND 2100 "
    "THEN make_date(TRY_CAST(tyear AS INTEGER), 12, 31) "
    "ELSE NULL END"
)
# GDP rows are a mix of quarterly (period 'Q1'..'Q4') and full-year ('Annual')
# records. Quarterly rows are dated to the first month of the quarter; 'Annual'
# rows (no quarter digit) fall back to year-end (Dec 31), which never collides
# with the Q4 date (Oct 1) of the same year.
_QUARTER_DATE = (
    "COALESCE("
    "make_date(TRY_CAST(tyear AS INTEGER), "
    "(TRY_CAST(regexp_extract(CAST(period AS VARCHAR), '[0-9]+') AS INTEGER) - 1) * 3 + 1, 1), "
    "make_date(TRY_CAST(tyear AS INTEGER), 12, 31))"
)

# 57 GDP sector/aggregate columns shared by Nominal & Real GDP (quarterly).
_GDP_NUM = [
    "agriculture", "cropProduction", "livestock", "forestry", "fishing", "industry",
    "miningAndQuarrying", "crudePetroleumAndNaturalGas", "coalMining", "metalOres",
    "quarryingAndOtherMinerals", "manufacturing", "oilRefining", "cement",
    "foodBeverageAndTobacco", "textileApparelAndFootwear", "woodAndWoodProducts",
    "pulpPaperAndPaperProducts", "chemicalAndPharmaceuticalProducts",
    "nonMetallicProducts", "plasticAndRubberProducts", "electricalAndElectronics",
    "basicMetalIronAndSteel", "motorVehiclesAndAssembly", "otherManufacturing",
    "electricityGasSteamAndAirCon", "waterSupplySewageWaste", "construction",
    "services", "trade", "accommodationAndFoodServices", "transportationAndStorage",
    "roadTransport", "railTransportAndPipelines", "waterTransport", "airTransport",
    "transportServices", "postAndCourierServices", "informationAndCommunication",
    "telecommunicationsAndInformationServices", "publishing",
    "motionPicturesSoundRecordingAndMusicProduction", "broadcasting",
    "artsEntertainmentAndRecreation", "financeAndInsurance", "financialInstitutions",
    "insurance", "realEstate", "professionalScientificAndTechnicalServices",
    "administrativeAndSupportServicesBusinessServices", "publicAdministration",
    "education", "humanHealthAndSocialServices", "otherServices",
    "gdPatCurrentBasicPrices", "netTaxesOnProducts", "gdPatCurrentMarketPrices",
]

# Securities datasets share one schema (auction-level records).
_SECURITIES = {
    "computed": {
        "date": _mdy_long("auctionDate"),
        # The source has occasional typo'd maturity years (e.g. a 91-day bill
        # auctioned 2007 with maturityDate 'December-27-2098'). A security
        # matures within its tenor of the auction (<=30y even for the longest
        # FGN bonds), so null any maturity that isn't within 40 years after the
        # auction date rather than letting typos pollute the series.
        "maturity_date": (
            f"CASE WHEN {_mdy_long('maturityDate')} BETWEEN {_mdy_long('auctionDate')} "
            f"AND ({_mdy_long('auctionDate')} + INTERVAL 40 YEAR) "
            f"THEN {_mdy_long('maturityDate')} END"
        ),
    },
    "text": ["securityType", "tenor", "auctionNo", "auction", "week",
             "rangeBid", "successfulBidRates", "rateDescription", "netType"],
    "num": ["totalSubscription", "totalSuccessful", "rate", "trueYield",
            "amtOffered", "totalAmtRepaid", "netValue"],
}

# Per-dataset column roles. `computed` maps output column -> raw SQL expression;
# `text` columns are kept as cleaned strings; `num` columns are cast to DOUBLE.
# The internal `id` and the raw date-source columns are intentionally dropped.
DATASETS = {
    "GetAllAssetsLiabilities": {
        "computed": {"date": _dmy("payDate")},
        "text": ["period"],
        "num": ["gold", "convertible", "imfGold", "sdr", "ter", "fgs", "osec",
                "redAdv", "otherAss", "fixAss", "totalAss", "liaCap", "genRes",
                "otherRes", "totalCap", "cbnInstruments", "cinC", "govtDep",
                "bankers", "others", "totalDep", "otherLia", "totalLia"],
    },
    "GetAllCrudeOilPrices": {
        "computed": {"date": _MONTHLY_DATE},
        "text": ["period"],
        "num": ["crudeOilPrice", "domProd", "crudeOilExp"],
    },
    "GetAllDailyCrude": {
        "computed": {"date": _dmy("postDate")},
        "text": [],
        "num": ["crudeOilPrice"],
    },
    "GetAllDiscountRates": {
        "computed": {"date": _dmy("ratedate")},
        "text": ["ratetype"],
        "num": ["amount"],
    },
    "GetAllExchangeRates": {
        "computed": {"date": _iso("ratedate")},
        "text": ["currency"],
        "num": ["buyingrate", "centralrate", "sellingrate"],
    },
    "GetAllFinancialData": {
        "computed": {"date": _dmy("recDate")},
        "text": [],
        "num": ["opeBal", "rediscBills", "slFacility", "sdFacility", "repo",
                "revRepo", "omoSales", "omoRepay", "pmSales", "pmRepay", "crr",
                "netWdas", "statAlloc", "jvCash", "netClr", "ndicPrem", "oMajor"],
    },
    "GetAllFiveYearStatement": {
        "computed": {"date": "make_date(TRY_CAST(year AS INTEGER), 12, 31)",
                     "year": "TRY_CAST(year AS INTEGER)"},
        "text": [],
        "num": ["extReserve", "holdingsSDR", "fedGovtSec", "rediscount",
                "otherAss", "otherSec", "exDiff", "fixedAss", "totalAss",
                "deposit", "cbnInst", "cinC", "imfsdr", "tradeDebt", "otherFore",
                "otherLia", "subLia", "shareCap", "genReserve", "assetsRev",
                "foreignC", "resFundInv", "subCapRes", "totalLia", "contingent",
                "totalIncome", "provisionforDebt", "operatnExp", "provision",
                "exceptional", "surplus", "appro", "transfer", "surplusFGN",
                "totalAppro"],
    },
    "GetAllInflationRates": {
        "computed": {"date": _MONTHLY_DATE},
        "text": ["period"],
        "num": ["allItemsYearOn", "allItemsAverage", "foodYearOn", "foodAverage",
                "allItemsLessFrmProdYearOn", "allItemsLessFrmProdAverage",
                "allItemsLessFrmProdAndEnergyYearOn",
                "allItemsLessFrmProdAndEnergyAvg"],
    },
    "GetAllIntPayments": {
        "computed": {"date": _dmy("payDate")},
        "text": [],
        "num": ["loc", "remit", "debt", "total"],
    },
    "GetAllInterbankRates": {
        "computed": {"date": _mdy_long("ratedate")},
        "text": ["ratetype", "range"],
        "num": ["weightedaverage"],
    },
    "GetAllMoneyAndCreditStats": {
        "computed": {"date": _MONTHLY_DATE},
        "text": ["period"],
        "num": ["moneySupply_M3", "cbnBills", "moneySupply_M2", "quasiMoney",
                "narrowMoney", "currencyOutsideBanks", "demandDeposits",
                "netForeignAssets", "netDomesticAssets", "netDomesticCredit",
                "creditToGovernment", "creditToGovernmentFed", "mirrorAccounts",
                "creditToPrivateSector", "otherAssetsNet", "baseMoney",
                "currencyInCirculation", "bankReserves",
                "specialInterventionReserves"],
    },
    "GetAllMoneyMarketIndicators": {
        "computed": {"date": _MONTHLY_DATE},
        "text": ["period"],
        "num": ["interBankCallRate", "mrr", "mpr", "treasuryBill",
                "savingsDeposit", "oneMonthDeposit", "threeMonthsDeposit",
                "sixMonthsDeposit", "twelveMonthsDeposit", "primeLending",
                "maxLending"],
    },
    "GetAllMonthlyAvgExchRates": {
        "computed": {"date": _MONTHLY_DATE},
        "text": ["period"],
        "num": ["daswdasDollar", "ifemDollar", "bdcDollar", "pounds", "euro",
                "cfaFr"],
    },
    "GetAllNominalGDP": {
        "computed": {"date": _QUARTER_DATE, "year": "TRY_CAST(tyear AS INTEGER)"},
        "text": ["period"],
        "num": list(_GDP_NUM),
    },
    "GetAllRealGDP": {
        "computed": {"date": _QUARTER_DATE, "year": "TRY_CAST(tyear AS INTEGER)"},
        "text": ["period"],
        "num": list(_GDP_NUM),
    },
    "GetAllReserves": {
        "computed": {"date": _dmy("moveDate")},
        "text": [],
        "num": ["gross", "liquid", "blocked", "blockPercent"],
    },
    "GetAllSecurities": _SECURITIES,
    "GetAllSecuritiesCBNBill": _SECURITIES,
    "GetAllSecuritiesFGNBond": _SECURITIES,
    "GetAllSecuritiesNTB": _SECURITIES,
    "GetAllSecuritiesOMO": _SECURITIES,
}


def _build_sql(entity_id: str, asset: str) -> str:
    cfg = DATASETS[entity_id]
    selects = [f"{expr} AS \"{name}\"" for name, expr in cfg["computed"].items()]
    selects += [_txt(c) for c in cfg["text"]]
    selects += [_num(c) for c in cfg["num"]]
    body = ",\n            ".join(selects)
    return f'SELECT\n            {body}\n        FROM "{asset}"'


TRANSFORM_SPECS = [
    SqlNodeSpec(
        id=f"{spec.id}-transform",
        deps=[spec.id],
        sql=_build_sql(_ENTITY_BY_SPEC[spec.id], spec.id),
    )
    for spec in DOWNLOAD_SPECS
]
