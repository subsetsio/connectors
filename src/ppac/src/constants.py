"""PPAC connector configuration — data, not logic.

ENTITY_IDS is the rank-accepted entity union (one published table each). The
two config maps describe how each entity is fetched: the 8 REST entities share
one generic AjaxController fetcher (page id + method + measure), the 5 XLSX
entities each have a dedicated parser keyed by entity id.
"""

# --- REST (AjaxController JSON) entities ------------------------------------
# entity_id -> page id, data method, reportBy (measure selector), unit label.
REST_CONFIG = {
    "consumption/products-wise": {
        "page_id": "43", "method": "getConsumptionPetroleumProductsData",
        "report_by": "1", "unit": "'000 Metric Tonnes",
    },
    "production/petroleum-products": {
        "page_id": "42", "method": "getPetroleumProductData",
        "report_by": "1", "unit": "'000 Metric Tonnes",
    },
    "prices/international-prices-of-crude-oil": {
        "page_id": "30", "method": "getInternationalPricesCrudeOil",
        "report_by": "4", "unit": "$/bbl",
    },
    "production/indigenous-crude-oil": {
        "page_id": "3", "method": "getProduction",
        "report_by": "1", "unit": "Million Metric Tonnes",
    },
    "import-export": {
        "page_id": "14", "method": "getImportExports",
        "report_by": "1", "unit": "'000 Metric Tonnes",
    },
    "natural-gas/production": {
        "page_id": "170", "method": "getGasProduction",
        "report_by": "4", "unit": "MMSCM",
    },
    "natural-gas/consumption": {
        "page_id": "138", "method": "getGasConsumption",
        "report_by": "4", "unit": "MMSCM",
    },
    "production/crude-processing": {
        "page_id": "41", "method": "getCrudeProcessingData",
        "report_by": "1", "unit": "'000 Metric Tonnes",
    },
}

# --- XLSX (download.php / uploads) entities ---------------------------------
# state -> value snapshot tables (one current value per state).
XLSX_SNAPSHOT = {
    "consumption/active-domestic-customers": {"unit": "Lakhs"},
    "consumption/state-wise-pmuy-data": {"unit": "Numbers"},
}
# entities with bespoke parsers (handled by dedicated fetch fns):
#   infrastructure/installed-refinery-capacity  -> fetch_refinery_capacity
#   consumption/state-wise                       -> fetch_statewise_consumption
#   natural-gas/import                           -> fetch_lng_import

ENTITY_IDS = [
    "consumption/active-domestic-customers",
    "consumption/products-wise",
    "consumption/state-wise",
    "consumption/state-wise-pmuy-data",
    "import-export",
    "infrastructure/installed-refinery-capacity",
    "natural-gas/consumption",
    "natural-gas/import",
    "natural-gas/production",
    "prices/international-prices-of-crude-oil",
    "production/crude-processing",
    "production/indigenous-crude-oil",
    "production/petroleum-products",
]
