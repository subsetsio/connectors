-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "lshhr",
    "month",
    "lmw_shr_lbyy_y",
    "environmental_indicator",
    "nw_lqym",
    "statistical_measure",
    "unit",
    "value"
FROM "qatar-planning-and-statistics-authority-monthly-environmental-indicators-doha-city"
