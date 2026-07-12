-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Rows include overlapping aggregate and subgroup strata; filter to one age, race, sex, stage, and rate type before aggregating year-level rates or counts.
SELECT
    "sex",
    "race",
    "age_range",
    "stage",
    "rate_type",
    "site",
    "year",
    "rate",
    "rate_lower_ci",
    "rate_upper_ci",
    "modeled_rate",
    "count"
FROM "seer-incidence-and-mortality-comparison-recent-trends"
