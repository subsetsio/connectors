-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Rows include age-specific mortality rates across overlapping race and sex strata; filter to one stratum before comparing rates or summing counts.
SELECT
    "sex",
    "race",
    "site",
    "age_range",
    "rate",
    "rate_lower_ci",
    "rate_upper_ci",
    "count",
    "rate_se"
FROM "seer-us-mortality-rates-by-age"
