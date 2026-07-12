-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "period",
    "nomenclature_on_the_countries_for_tourism_statistics_purposes",
    "indicators",
    "unit",
    "value"
FROM "statistics-bulgaria-159"
