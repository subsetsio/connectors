"""Static catalog data for the CBE connector (data, not logic).

ENTITY_IDS is the rank-active entity union (one publishable dataset each),
copied verbatim from data/sources/cbe/work/entity_union.json. Each id is
"<category-slug>__<dataset-slug>"; the dataset's XLSX files live under
/-/media/project/cbe/listing/time-series/<category-slug>/<dataset-slug>/.

CAT_SLUG_TO_GUID maps each category slug to the GUID of the Time-Series
"download list" page that enumerates that category's XLSX file links.
"""

ENTITY_IDS = [
    "banking-survey__deposits-in-local-and-foreign-currency",
    "banking-survey__domestic-credit",
    "banking-survey__domestic-liquidity-and-counterpart-assets",
    "banking-survey__foreign-assets-and-liabilities",
    "banking-survey__net-balancing-item",
    "bop__egypts-balance-of-payments",
    "cbe__central-bank-of-egypt-clearing-house-activities",
    "cbe__currency-in-circulation-outside-cbe-by-denomination",
    "cbe__note-issued-including-cash-in-cbe-vault-by-denomination",
    "cbe__reserve-money-and-counterpart-assets",
    "domestic-debt__domestic-debt-of-government-and-economic-authorities-debt",
    "domestic-debt__national-investment-bank",
    "domestic-debt__the-outstanding-balance-of-treasury-bills-quarterly",
    "external-debt__external-debt-and-indicators",
    "external-debt__external-debt-by-debtor",
    "foreign-trade__exports-by-geographical-distribution",
    "foreign-trade__imports-by-geographical-distribution",
    "foreign-trade__main-merchandise-balances",
    "foreign-trade__payments-for-merchandise-imports-by-degree-of-use",
    "foreign-trade__proceeds-of-merchandise-exports-by-degree-of-processing",
    "gdp__gdp-at-factor-cost-constant",
    "gdp__gdp-at-factor-cost-current",
    "gdp__gdp-by-expenditure-constant",
    "gdp__gdp-by-expenditure-current",
    "inflation__cpi",
    "inflation__wpi-and-ppi",
    "interest-rates__domestic-interest-rates-on-3-months-deposits-of-major-currencies",
    "interest-rates__the-discount-rate-and-interest-rates-on-deposits-and-loans-in-egyptian-pounds",
    "investments__investments-by-economic-sectors",
    "state-budget__deficit-and-sources-of-financing",
    "state-budget__expenditures",
    "state-budget__revenues",
    "stock__stock-market-main-indicators",
    "time-series__net-foreign-direct-investment",
]

# category slug -> Time-Series download-list page GUID (the page that lists the
# category's per-dataset XLSX <a href> links). Verified live during research.
CAT_SLUG_TO_GUID = {
    "cbe": "099EFD590A274C8F9259740B4FE96AAD",
    "domestic-debt": "F016705643D24C51959577587914DA5C",
    "external-debt": "2596CC0C64D5474C865C49E48A24D483",
    "gdp": "DEF6421CA1354B128A1113D7A5BBFC66",
    "interest-rates": "909707CDAD5C47529817D6146659E054",
    "investments": "A6ACD7B25BE64045A90660B320ECFA32",
    "time-series": "623F34508AE148C1969795A8F78FDA49",
    "foreign-trade": "F0324992E95741438C789A669E5194F4",
    "stock": "3EB4667B01F04C41ADCF7D96039037A4",
    "banking-survey": "F9F37F0E98A54C3684790C4037AA4BE3",
    "bop": "232131B16F15454BB1E1933B2BFEB041",
    "inflation": "706A9057F8454F7284BE8143070D88C4",
    "state-budget": "97805EA8534C4134B65BDE9621E187AF",
}
