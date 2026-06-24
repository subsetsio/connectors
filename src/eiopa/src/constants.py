# Entity union (rank-active collect entities) and the source-file map.
# This is DATA (which files back each subset), not logic — kept out of the node
# module per the implement contract.

ENTITY_IDS = [
    "financial-stability-indicators",
    "group-balance-sheet",
    "group-own-funds",
    "group-premiums-claims-expenses",
    "solo-asset-exposures",
    "solo-balance-sheet",
    "solo-own-funds",
    "solo-premiums-claims-expenses",
]

BASE_URL = (
    "https://nexteuropa-multisites.s3.eu-west-1.amazonaws.com/"
    "www.eiopa.europa.eu/assets/insurance-statistics"
)

# Generic long-format CSV blocks. Each entity unions one or more stable bulk
# files; frequency is carried as a column. Within an entity every file shares a
# column list (verified against live headers). Solo files key on "Reporting
# country" + "Undertaking type"; group files key on "Region" (no undertaking type).
CSV_FILES = {
    "solo-balance-sheet": [("SQ_Balance_Sheet", "quarterly"), ("SA_Balance_Sheet", "annual")],
    "group-balance-sheet": [("GQ_Balance_Sheet", "quarterly"), ("GA_Balance_Sheet", "annual")],
    "solo-own-funds": [("SQ_Own_Funds", "quarterly"), ("SA_Own_Funds", "annual")],
    "group-own-funds": [("GQ_Own_Funds", "quarterly"), ("GA_Own_Funds", "annual")],
    # Premiums/claims/expenses: only the quarterly file is on the stable bulk
    # path (annual is behind register redirects).
    "solo-premiums-claims-expenses": [("SQ_Premiums_Claims_Expenses", "quarterly")],
    "group-premiums-claims-expenses": [("GQ_Premiums_Claims_Expenses", "quarterly")],
}

# XLSX-only blocks (no CSV variant published).
EXPOSURE_FILE = "SQ_Exposure"          # solo-asset-exposures
FS_FILE = "FS_Indicators"              # financial-stability-indicators
