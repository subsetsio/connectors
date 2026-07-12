-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Rows include overlapping race and sex strata; filter to one stratum before comparing median age or summing counts.
SELECT
    "sex",
    "race",
    "site",
    "median_age",
    "count"
FROM "seer-seer-incidence-median-age"
