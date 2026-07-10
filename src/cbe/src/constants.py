"""Static catalog data for the CBE connector (data, not logic).

ENTITY_IDS is the rank-active entity union (one publishable dataset each),
copied verbatim from data/sources/cbe/work/entity_union.json. Each id is
"<category-slug>__<dataset-slug>"; the dataset's XLSX files live under
/-/media/project/cbe/listing/time-series/<category-slug>/<dataset-slug>/.

CAT_SLUG_TO_GUID maps each category slug to the GUID of the Time-Series
"download list" page that enumerates that category's XLSX file links.
"""

ENTITY_IDS = [
    "bop__egypts-balance-of-payments",
    "domestic-debt__the-outstanding-balance-of-treasury-bills-quarterly",
    "external-debt__external-debt-and-indicators",
    "external-debt__external-debt-by-debtor",
    "foreign-trade__exports-by-geographical-distribution",
    "foreign-trade__imports-by-geographical-distribution",
    "foreign-trade__main-merchandise-balances",
    "foreign-trade__payments-for-merchandise-imports-by-degree-of-use",
    "foreign-trade__proceeds-of-merchandise-exports-by-degree-of-processing",
    "inflation__cpi",
    "inflation__wpi-and-ppi",
    "state-budget__deficit-and-sources-of-financing",
    "state-budget__expenditures",
    "state-budget__revenues",
    "time-series__net-foreign-direct-investment",
    "tourism__number-of-tourist-nights",
    "tourism__number-of-tourists",
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
    "tourism": "B928771A1D1A4550A1B08F9386DDC0FA",
}
