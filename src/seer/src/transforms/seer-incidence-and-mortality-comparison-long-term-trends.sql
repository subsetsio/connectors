-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Rows include overlapping aggregate and subgroup strata such as all races/sexes/ages and individual groups; filter to one stratum before aggregating rates, modeled rates, or counts.
SELECT
    "sex",
    "race",
    "age_range",
    "rate_type",
    "site",
    "year",
    "rate",
    "rate_lower_ci",
    "rate_upper_ci",
    "modeled_rate",
    "count"
FROM "seer-incidence-and-mortality-comparison-long-term-trends"
