-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Rows include overlapping aggregate and subgroup strata, including cancer subtypes; filter to one stratum before aggregating year-level incidence rates or counts.
SELECT
    "rate_type",
    "sex",
    "race",
    "age_range",
    "subtype",
    "site",
    "year",
    "rate",
    "rate_lower_ci",
    "rate_upper_ci",
    "modeled_rate",
    "count"
FROM "seer-seer-incidence-long-term-trends"
