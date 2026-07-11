-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "mean_age_of_childbearing",
    "year",
    "value"
FROM "geostat-demography-births-17-mean-age-of-childbearing-total-and-first"
