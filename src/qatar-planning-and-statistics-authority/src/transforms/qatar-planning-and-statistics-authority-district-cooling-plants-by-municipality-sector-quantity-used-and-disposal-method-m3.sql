-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "cooling_plant_discharge_method",
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
    "slwb_ltkhls_mn_myh_mhtt_ltbryd_lmrfwd",
    "geo_point",
    "geo_shape"
FROM "qatar-planning-and-statistics-authority-district-cooling-plants-by-municipality-sector-quantity-used-and-disposal-method-m3"
