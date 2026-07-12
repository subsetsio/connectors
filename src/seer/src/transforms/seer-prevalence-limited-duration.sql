-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Rows include overlapping demographic strata and prevalence-duration categories; filter to one stratum before aggregating counts or percentages.
SELECT
    "sex",
    "race",
    "age_range",
    "prev_duration",
    "site",
    "count",
    "percent",
    "aa_percent"
FROM "seer-prevalence-limited-duration"
