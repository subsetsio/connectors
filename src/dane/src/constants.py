# The rank-accepted entity union for the DANE connector.
# Copied from data/sources/dane/work/entity_union.json.
#
# Scope: this initial build publishes DANE's cleanly-structured, recurring
# SIPSA price & supply time-series (Sistema de Informacion de Precios y
# Abastecimiento del Sector Agropecuario). The remaining ~560 DANE microdata
# studies are raw, schema-drifting, dictionary-coded survey microdata (often
# multi-GB, one-off survey years) that are not cleanly publishable without
# per-study normalization; they are deferred for curator review.
ENTITY_IDS = [
    "DANE-DIMPE-SIPSA-P-2013-2024",   # wholesale food prices (monthly/daily, by product x market)
    "DANE-DIMPE-SIPSA-A-2018-2025",   # food supply / abastecimiento (by city, dept, product)
]

# NADA numeric catalog id per entity (the per-study download URLs key off this,
# NOT the alphanumeric idno). Verified live against the catalog.
CATALOG_NUMERIC_ID = {
    "DANE-DIMPE-SIPSA-P-2013-2024": "776",
    "DANE-DIMPE-SIPSA-A-2018-2025": "697",
}
