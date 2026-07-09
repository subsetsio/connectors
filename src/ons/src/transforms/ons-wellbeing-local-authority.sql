-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "value",
    "data_marking",
    "lower_limit",
    "upper_limit",
    "yyyy_yy",
    "time",
    "administrative_geography",
    "geography",
    "measure_of_wellbeing",
    "measureofwellbeing",
    "wellbeing_estimate",
    "estimate"
FROM "ons-wellbeing-local-authority"
