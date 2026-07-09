"""Data, not logic: which Atlas entities we pull, and where each one's files live.

Every entity is one Harvard Dataverse dataset (addressed by its stable DOI) plus
a filename prefix selecting the files that make it up. The numeric dataFile ids
are NOT here on purpose — they change on every republish, so the node module
resolves them at fetch time from the dataset's file manifest.

`prefix` is matched with str.startswith against the filename. It is grain-shaped
rather than an exact filename list, so a re-release that adds a product depth
(`hs22_country_product_year_6.csv`) lands in the right entity with no code
change. The prefixes cannot collide: `hs92_country_year` does not prefix
`hs92_country_country_year`, and `hs92_country_product_year_` does not prefix
`hs92_country_country_product_year_6_1995_1999`.

The six bilateral country x partner x product x year entities are deliberately
absent — they are ~53 GB of CSV and the accept stage deferred them
(soft_too_large).
"""

HS92 = "doi:10.7910/DVN/T4CHWJ"  # International Trade Data (HS, 92)
HS12 = "doi:10.7910/DVN/YAVJDF"  # International Trade Data (HS, 12)
HS22 = "doi:10.7910/DVN/FTUUJU"  # International Trade Data (HS, 22)
SITC = "doi:10.7910/DVN/H8SFD2"  # International Trade Data (SITC, Rev. 2)
SERVICES = "doi:10.7910/DVN/NDDMSN"  # International Trade Data (Services)
CLASSIFICATIONS = "doi:10.7910/DVN/3BAL1O"  # Classifications Data
PRODUCT_SPACE = "doi:10.7910/DVN/FCDZBN"  # Product Space Networks
GROWTH_PROJ = "doi:10.7910/DVN/XTAQMC"  # Growth Projections and Complexity Rankings
CONVERSION = "doi:10.7910/DVN/6AADMR"  # Weighted HS <-> SITC Conversion Tables

# entity_id -> {doi, prefix, layout?}
#   layout "conversion" reshapes the heterogeneous source/target mapping files
#   into one uniform table; everything else is written as published, under a
#   union schema. See the node module.
ENTITIES: dict[str, dict[str, str]] = {
    # --- Goods trade, one block per classification -------------------------
    "hs92-country-year": {"doi": HS92, "prefix": "hs92_country_year"},
    "hs92-country-country-year": {"doi": HS92, "prefix": "hs92_country_country_year"},
    "hs92-country-product-year": {"doi": HS92, "prefix": "hs92_country_product_year_"},
    "hs92-product-year": {"doi": HS92, "prefix": "hs92_product_year_"},
    "hs12-country-year": {"doi": HS12, "prefix": "hs12_country_year"},
    "hs12-country-country-year": {"doi": HS12, "prefix": "hs12_country_country_year"},
    "hs12-country-product-year": {"doi": HS12, "prefix": "hs12_country_product_year_"},
    "hs12-product-year": {"doi": HS12, "prefix": "hs12_product_year_"},
    "hs22-country-year": {"doi": HS22, "prefix": "hs22_country_year"},
    "hs22-country-country-year": {"doi": HS22, "prefix": "hs22_country_country_year"},
    "hs22-country-product-year": {"doi": HS22, "prefix": "hs22_country_product_year_"},
    "hs22-product-year": {"doi": HS22, "prefix": "hs22_product_year_"},
    "sitc-country-year": {"doi": SITC, "prefix": "sitc_country_year"},
    "sitc-country-country-year": {"doi": SITC, "prefix": "sitc_country_country_year"},
    "sitc-country-product-year": {"doi": SITC, "prefix": "sitc_country_product_year_"},
    "sitc-product-year": {"doi": SITC, "prefix": "sitc_product_year_"},
    # --- Services trade ----------------------------------------------------
    "services-unilateral-country-year": {
        "doi": SERVICES, "prefix": "services_unilateral_country_year"},
    "services-unilateral-country-product-year": {
        "doi": SERVICES, "prefix": "services_unilateral_country_product_year_"},
    "services-unilateral-product-year": {
        "doi": SERVICES, "prefix": "services_unilateral_product_year_"},
    # --- Reference / dimension tables --------------------------------------
    "location-country": {"doi": CLASSIFICATIONS, "prefix": "location_country"},
    "location-group": {"doi": CLASSIFICATIONS, "prefix": "location_group"},
    "product-hs92": {"doi": CLASSIFICATIONS, "prefix": "product_hs92"},
    "product-hs12": {"doi": CLASSIFICATIONS, "prefix": "product_hs12"},
    "product-hs22": {"doi": CLASSIFICATIONS, "prefix": "product_hs22"},
    "product-sitc": {"doi": CLASSIFICATIONS, "prefix": "product_sitc"},
    "product-services-unilateral": {
        "doi": CLASSIFICATIONS, "prefix": "product_services_unilateral"},
    "top-edges-hs92": {"doi": PRODUCT_SPACE, "prefix": "top_edges_hs92"},
    "umap-layout-hs92": {"doi": PRODUCT_SPACE, "prefix": "umap_layout_hs92"},
    "growth-proj-eci-rankings": {"doi": GROWTH_PROJ, "prefix": "growth_proj_eci_rankings"},
    # Every file in the conversion dataset is one (source -> target) mapping,
    # so the prefix matches all of them and they fold into one table.
    "weighted-classification-conversion-tables": {
        "doi": CONVERSION, "prefix": "", "layout": "conversion"},
}

ENTITY_IDS = list(ENTITIES)
