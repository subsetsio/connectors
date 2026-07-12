-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "item",
    "municipality",
    "other",
    "industrial",
    "real_estate_development",
    "sport",
    "cultural",
    "health",
    "transport",
    "education",
    "hotels",
    "commercial",
    "district_cooling_service_supply",
    "lbldy",
    "lbyn",
    "geo_point",
    "geo_shape"
FROM "qatar-planning-and-statistics-authority-cooling-energy-consumption-and-savings-by-municipality-and-economic-activity-mwh"
