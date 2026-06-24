"""Static data for the Federal Reserve Bank of Atlanta connector.

ENTITY_IDS is the rank-accepted entity union (copied from
data/sources/federal-reserve-bank-of-atlanta/work/entity_union.json).
URLS maps each entity to its stable CDN data-file URL (discovered by scraping
the per-product pages under atlantafed.org/research-and-data/data/<slug>).
The two China entities are served as point-in-time dated ZIP releases, so their
URL is discovered at fetch time rather than pinned here.
"""

ENTITY_IDS = [
    "china-gdp-consumption",
    "china-macroeconomy",
    "commercial-real-estate-market-index",
    "deflation-probabilities",
    "gdp-based-recession-indicator-index",
    "gdpnow",
    "home-ownership-affordability-monitor",
    "labor-force-participation-dynamics",
    "market-probability-tracker",
    "sticky-price-cpi",
    "taylor-rule",
    "underlying-inflation-dashboard",
    "wage-growth-tracker",
    "wu-xia-shadow-federal-funds-rate",
]

_BASE = "https://www.atlantafed.org"

URLS = {
    "commercial-real-estate-market-index": _BASE
    + "/-/media/Project/Atlanta/FRBA/Documents/research/housing-and-policy/cremi/CREMI_CBSA_Results.csv",
    "deflation-probabilities": _BASE
    + "/-/media/Project/Atlanta/FRBA/Documents/datafiles/research/inflationproject/dp/DeflationProbabilities.xlsx",
    "gdp-based-recession-indicator-index": "https://www.econbrowser.com/wp-content/uploads/2014/04/Real_time_decision_rules.xls",
    "gdpnow": _BASE
    + "/-/media/Project/Atlanta/FRBA/Documents/cqer/researchcq/gdpnow/GDPTrackingModelDataAndForecasts.xlsx",
    "home-ownership-affordability-monitor": _BASE
    + "/-/media/Project/Atlanta/FRBA/Documents/research/housing-and-policy/hoam/HOAM_CBSA_Data.xlsx",
    "labor-force-participation-dynamics": _BASE
    + "/-/media/Project/Atlanta/FRBA/Documents/datafiles/chcs/labor-force-participation-dynamics/labor-force-participation-dynamics-trends-over-time-data-download.xlsx",
    "market-probability-tracker": _BASE
    + "/-/media/Project/Atlanta/FRBA/Documents/cenfis/market-probability-tracker/mpt_histdata.xlsx",
    "sticky-price-cpi": _BASE
    + "/-/media/Project/Atlanta/FRBA/Documents/datafiles/research/inflationproject/stickprice/stickyprice.xlsx",
    "taylor-rule": _BASE
    + "/-/media/Project/Atlanta/FRBA/Documents/datafiles/cqer/research/taylor-rule/taylor-rule-data.xlsx",
    "underlying-inflation-dashboard": _BASE
    + "/-/media/Project/Atlanta/FRBA/Documents/datafiles/research/inflationproject/underlying-inflation-dashboard/underlying-inflation-dashboard-data.xlsx",
    "wage-growth-tracker": _BASE
    + "/-/media/Project/Atlanta/FRBA/Documents/datafiles/chcs/wage-growth-tracker/wage-growth-data.xlsx",
    "wu-xia-shadow-federal-funds-rate": _BASE
    + "/-/media/Project/Atlanta/FRBA/Documents/datafiles/cqer/research/wu-xia-shadow-federal-funds-rate/WuXiaShadowRate.xlsx",
}

# Page scraped to discover the latest dated China macroeconomy ZIP release.
CHINA_PAGE = _BASE + "/cqer/research/china-macroeconomy"
