# Entity union for the Chicago Fed connector — copied from
# data/sources/chicagofed/work/entity_union.json (rank-active subsets).
# These are <PROVIDER>/<file-stem> pairs; the data CSV for each lives at
# https://api.data.chicagofed.org/<PROVIDER>/<file-stem>.csv

ENTITY_IDS = [
    "Agriculture/Ag-Credit-Conditions",
    "Agriculture/Farmland-Values",
    "Agriculture/New-Farm-Loans-Interest",
    "Agriculture/seventh-district-ag-real-estate",
    "CARTS/carts-dashboard-fig1",
    "CARTS/carts-dashboard-fig3",
    "CARTS/retail-and-food-services-prices-ex-auto-csv",
    "CARTS/retail_and_food_services_sales_ex_auto",
    "CFLMI/table",
    "CFNAI/cfnai-data-series-csv",
    "CFNAI/cfnai-shading-csv",
    "CFSEC/cfsec-activity-index-csv",
    "NFCI/anfci-decomposed-csv",
    "NFCI/nfci-chart-series-csv",
    "NFCI/nfci-data-series-csv",
    "NFCI/nfci-decomposed-csv",
]

# Most files are wide tables whose FIRST column is the period/date key. A few
# are record tables where the period key is a named column; override here.
PERIOD_COL_OVERRIDES = {
    "CFLMI/table": "Period Date",
}
