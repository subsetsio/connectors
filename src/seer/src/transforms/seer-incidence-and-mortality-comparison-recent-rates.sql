-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Rows include overlapping aggregate and subgroup strata, including stage and age groups; filter to one stratum before aggregating rates or counts.
SELECT
    "sex",
    "race",
    "age_range",
    "stage",
    "data_type",
    "site",
    "rate",
    "rate_se",
    "rate_lower_ci",
    "rate_upper_ci",
    "count"
FROM "seer-incidence-and-mortality-comparison-recent-rates"
