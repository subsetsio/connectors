"""Dataset-id selections for the central-bank-of-nigeria connector.

These lists name which datasets/entities the connector pulls. They are data, not
logic, so they live here instead of being hardcoded in the node module(s), and are
imported back as e.g. ``from constants import ENTITY_IDS``.

This file sits outside ``nodes/`` on purpose: ``load_nodes`` only scans ``nodes/``,
so it is never treated as a node module, and the runner puts ``src/`` on the path
so the import resolves at validation and at runtime.
"""


ENTITY_IDS = [
    "GetAllAssetsLiabilities",
    "GetAllCrudeOilPrices",
    "GetAllDailyCrude",
    "GetAllDiscountRates",
    "GetAllExchangeRates",
    "GetAllFinancialData",
    "GetAllFiveYearStatement",
    "GetAllInflationRates",
    "GetAllIntPayments",
    "GetAllInterbankRates",
    "GetAllMoneyAndCreditStats",
    "GetAllMoneyMarketIndicators",
    "GetAllMonthlyAvgExchRates",
    "GetAllNominalGDP",
    "GetAllRealGDP",
    "GetAllReserves",
    "GetAllSecurities",
    "GetAllSecuritiesCBNBill",
    "GetAllSecuritiesFGNBond",
    "GetAllSecuritiesNTB",
    "GetAllSecuritiesOMO",
]
