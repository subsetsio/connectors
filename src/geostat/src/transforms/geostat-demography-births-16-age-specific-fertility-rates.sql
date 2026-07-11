-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "age_of_mother",
    "year",
    "value"
FROM "geostat-demography-births-16-age-specific-fertility-rates"
