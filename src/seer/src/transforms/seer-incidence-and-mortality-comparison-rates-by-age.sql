-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Rows include age-specific rates across overlapping race/sex strata; filter to one race, sex, and rate type before comparing rates or summing counts.
SELECT
    "sex",
    "race",
    "rate_type",
    "site",
    "age_range",
    "rate",
    "rate_lower_ci",
    "rate_upper_ci",
    "count",
    "rate_se"
FROM "seer-incidence-and-mortality-comparison-rates-by-age"
