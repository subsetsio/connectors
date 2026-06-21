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

# Fallback download resource ids per numeric catalog id, snapshotted from the
# get-microdata page on 2026-06-21. The fetch fn prefers a live scrape of that
# page (so new releases are picked up automatically), but DANE's WAF 403s the
# HTML page from some datacenter IPs (the page is reCAPTCHA-protected) while the
# /download/<rid> endpoint stays reachable. This list is the resilient fallback
# so a run still succeeds when the page is blocked. Refresh it if the source
# republishes under new resource ids (the live scrape covers that when reachable).
FALLBACK_RESOURCE_IDS = {
    "776": [  # SIPSA-P wholesale prices, one ZIP per year
        "23891", "23892", "23893", "23894",
        "23895", "23896", "23897", "23898",
    ],
    "697": [  # SIPSA-A supply, one ZIP per semester/cuatrimestre
        "20281", "20282", "20283", "20284", "20285", "20286",
        "20536", "21267", "21418", "22198", "22886", "23116",
        "23637", "23638", "23771", "24171", "24294", "24413", "24690",
    ],
}
