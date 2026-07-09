"""Dataset selections for the central-bank-of-nigeria connector.

`ENDPOINTS` maps each accepted entity id (the friendly, lower-cased hyphen form
from the entity union at data/sources/central-bank-of-nigeria/work/entity_union.json)
to its `GetAll<Dataset>` path on the CBN statistics REST API. It is data, not
logic — which datasets we pull, not how — so it lives here instead of in the node
module, and is imported back as ``from constants import ENDPOINTS``.

This file sits outside ``nodes/`` on purpose: ``load_nodes`` only scans ``nodes/``,
so it is never treated as a node module, and the runner puts ``src/`` on the path
so the import resolves at validation and at runtime.
"""


ENDPOINTS = {
    "crude-oil-price-daily":        "GetAllDailyCrude",
    "crude-oil-prices-monthly":     "GetAllCrudeOilPrices",
    "daily-financial-data":         "GetAllFinancialData",
    "exchange-rates-daily":         "GetAllExchangeRates",
    "inflation-rates":              "GetAllInflationRates",
    "interbank-rates":              "GetAllInterbankRates",
    "money-and-credit-statistics":  "GetAllMoneyAndCreditStats",
    "money-market-indicators":      "GetAllMoneyMarketIndicators",
    "nafem-nof-rates":              "GetAllNOF_Rates",
    "nominal-gdp-annual":           "GetAllYearsNominalGDP",
    "nominal-gdp-quarterly":        "GetAllNominalGDP",
    "real-gdp-annual":              "GetAllYearsRealGDP",
    "real-gdp-quarterly":           "GetAllRealGDP",
    "securities-auctions":          "GetAllSecurities",
}
