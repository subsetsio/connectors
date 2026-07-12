-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Rows include overlapping demographic strata and rural/urban classifications; filter to one stratum before aggregating year-level mortality rates or counts.
SELECT
    "rucc",
    "sex",
    "race",
    "age_range",
    "site",
    "year",
    "rate",
    "rate_lower_ci",
    "rate_upper_ci",
    "modeled_rate",
    "count"
FROM "seer-us-mortality-rural-urban-trends"
