-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "lmw_shr_lmnkhy",
    "climate_indicator",
    "nw_lqym",
    "statistical_measure",
    "unit",
    "value"
FROM "qatar-planning-and-statistics-authority-annual-relative-humidity-and-rainfall-qatar"
