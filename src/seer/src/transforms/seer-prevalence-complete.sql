-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Rows include overlapping age and sex strata; filter to one stratum before aggregating complete-prevalence counts or percentages.
SELECT
    "sex",
    "age_range",
    "site",
    "count",
    "percent"
FROM "seer-prevalence-complete"
