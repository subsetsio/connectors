# Entity union for the Chicago Fed connector — copied from
# data/sources/chicagofed/work/entity_union.json (rank-active subsets).
# ENTITY_URLS maps each entity id to its stable source CSV URL
# (https://api.data.chicagofed.org/<PROVIDER>/<file>.csv).

ENTITY_URLS = {
    'Agriculture-Ag-Credit-Conditions': 'https://api.data.chicagofed.org/Agriculture/Ag-Credit-Conditions.csv',
    'Agriculture-Farmland-Values': 'https://api.data.chicagofed.org/Agriculture/Farmland-Values.csv',
    'Agriculture-New-Farm-Loans-Interest': 'https://api.data.chicagofed.org/Agriculture/New-Farm-Loans-Interest.csv',
    'Agriculture-seventh-district-ag-real-estate': 'https://api.data.chicagofed.org/Agriculture/seventh-district-ag-real-estate.csv',
    'CARTS-carts-dashboard-fig1': 'https://api.data.chicagofed.org/CARTS/carts-dashboard-fig1.csv',
    'CARTS-carts-dashboard-fig3': 'https://api.data.chicagofed.org/CARTS/carts-dashboard-fig3.csv',
    'CARTS-retail-and-food-services-prices-ex-auto-csv': 'https://api.data.chicagofed.org/CARTS/retail-and-food-services-prices-ex-auto-csv.csv',
    'CARTS-retail_and_food_services_sales_ex_auto': 'https://api.data.chicagofed.org/CARTS/retail_and_food_services_sales_ex_auto.csv',
    'CFLMI-table': 'https://api.data.chicagofed.org/CFLMI/table.csv',
    'CFNAI-cfnai-data-series-csv': 'https://api.data.chicagofed.org/CFNAI/cfnai-data-series-csv.csv',
    'CFNAI-cfnai-shading-csv': 'https://api.data.chicagofed.org/CFNAI/cfnai-shading-csv.csv',
    'CFSEC-cfsec-activity-index-csv': 'https://api.data.chicagofed.org/CFSEC/cfsec-activity-index-csv.csv',
    'NFCI-anfci-decomposed-csv': 'https://api.data.chicagofed.org/NFCI/anfci-decomposed-csv.csv',
    'NFCI-nfci-chart-series-csv': 'https://api.data.chicagofed.org/NFCI/nfci-chart-series-csv.csv',
    'NFCI-nfci-data-series-csv': 'https://api.data.chicagofed.org/NFCI/nfci-data-series-csv.csv',
    'NFCI-nfci-decomposed-csv': 'https://api.data.chicagofed.org/NFCI/nfci-decomposed-csv.csv',
}

ENTITY_IDS = list(ENTITY_URLS)

# Files whose period/date key is a named column rather than column 1.
PERIOD_COL_OVERRIDES = {
    "CFLMI-table": "Period Date",
}
