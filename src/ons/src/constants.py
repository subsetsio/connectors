"""Dataset-id selections for the ons connector.

These lists name which datasets/entities the connector pulls. They are data, not
logic, so they live here instead of being hardcoded in the node module(s), and are
imported back as e.g. ``from constants import ENTITY_IDS``.

This file sits outside ``nodes/`` on purpose: ``load_nodes`` only scans ``nodes/``,
so it is never treated as a node module, and the runner puts ``src/`` on the path
so the import resolves at validation and at runtime.
"""


ENTITY_IDS = [
    "ST001", "ST002", "ST003", "ST004", "ST005", "ST006", "ST007", "ST008",
    "ST009", "ST010", "ST011", "ST012", "ST013",
    "TS001", "TS002", "TS003", "TS004", "TS005", "TS006", "TS007", "TS008",
    "TS009", "TS010", "TS011", "TS012", "TS013", "TS015", "TS016", "TS017",
    "TS018", "TS019", "TS020", "TS021", "TS022", "TS023", "TS024", "TS025",
    "TS026", "TS027", "TS028", "TS029", "TS030", "TS031", "TS032", "TS033",
    "TS034", "TS035", "TS036", "TS037", "TS037ASP", "TS038", "TS038ASP",
    "TS039", "TS039ASP", "TS040", "TS041", "TS044", "TS045", "TS046", "TS047",
    "TS048", "TS050", "TS051", "TS052", "TS053", "TS054", "TS055", "TS056",
    "TS058", "TS059", "TS060", "TS061", "TS062", "TS063", "TS064", "TS065",
    "TS066", "TS067", "TS068", "TS070", "TS071", "TS072", "TS073", "TS074",
    "TS075", "TS076", "TS077", "TS078", "TS079",
    "ageing-population-estimates", "ageing-population-projections",
    "ashe-table-5", "ashe-tables-11-and-12", "ashe-tables-20", "ashe-tables-25",
    "ashe-tables-26", "ashe-tables-27-and-28", "ashe-tables-3",
    "ashe-tables-7-and-8", "ashe-tables-9-and-10", "childrens-wellbeing",
    "cpih01", "faster-indicators-shipping-data", "gdp-by-local-authority",
    "gdp-to-four-decimal-places", "generational-income",
    "gva-by-industry-by-local-authority", "health-accounts",
    "house-prices-local-authority", "index-private-housing-rental-prices",
    "labour-market", "life-expectancy-by-local-authority", "mid-year-pop-est",
    "older-people-economic-activity", "older-people-net-internal-migration",
    "older-people-sex-ratios", "online-job-advert-estimates",
    "output-in-the-construction-industry",
    "projections-older-people-in-single-households",
    "projections-older-people-sex-ratios", "regional-gdp-by-quarter",
    "regional-gdp-by-year", "retail-sales-index",
    "retail-sales-index-all-businesses",
    "retail-sales-index-large-and-small-businesses",
    "sexual-orientation-by-age-and-sex", "sexual-orientation-by-region",
    "suicides-in-the-uk", "tax-benefits-statistics", "trade",
    "traffic-camera-activity", "uk-business-by-enterprises-and-local-units",
    "uk-spending-on-cards", "weekly-deaths-age-sex", "weekly-deaths-health-board",
    "weekly-deaths-local-authority", "weekly-deaths-region",
    "wellbeing-local-authority", "wellbeing-quarterly",
]
