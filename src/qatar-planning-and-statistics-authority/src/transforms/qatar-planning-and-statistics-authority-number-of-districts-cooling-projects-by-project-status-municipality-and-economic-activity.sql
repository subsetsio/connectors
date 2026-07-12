-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "project_status",
    "municipality",
    "other",
    "industrial",
    "real_estate_development",
    "sport",
    "culture",
    "health",
    "transport",
    "education",
    "hotels",
    "commercial",
    "district_cooling_service_supply",
    "lbldy",
    "hl_lmshry",
    "geo_point",
    "geo_shape"
FROM "qatar-planning-and-statistics-authority-number-of-districts-cooling-projects-by-project-status-municipality-and-economic-activity"
