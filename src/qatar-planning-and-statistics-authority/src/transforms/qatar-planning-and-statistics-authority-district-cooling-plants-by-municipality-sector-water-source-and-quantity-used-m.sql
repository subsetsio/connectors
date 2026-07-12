-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "source_of_compensatory_cooling_water",
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
    "msdr_myh_ltbryd_lt_wydy",
    "geo_point",
    "geo_shape"
FROM "qatar-planning-and-statistics-authority-district-cooling-plants-by-municipality-sector-water-source-and-quantity-used-m"
