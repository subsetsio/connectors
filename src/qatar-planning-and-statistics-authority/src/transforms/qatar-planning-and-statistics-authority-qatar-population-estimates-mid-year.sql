-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "population_metric_ar",
    "population_indicator_type",
    "value",
    "annual_growth_rate"
FROM "qatar-planning-and-statistics-authority-qatar-population-estimates-mid-year"
