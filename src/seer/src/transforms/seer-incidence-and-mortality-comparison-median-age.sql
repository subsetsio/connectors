-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Rows include overlapping aggregate and subgroup strata such as all races and individual race groups; filter to one stratum before comparing median age or summing counts.
SELECT
    "sex",
    "race",
    "data_type",
    "site",
    "median_age",
    "count"
FROM "seer-incidence-and-mortality-comparison-median-age"
