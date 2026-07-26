-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "metric_name",
    "program_target_population",
    "category",
    "subgroup",
    "period_type",
    "period",
    "metric_value"
FROM "nyc-open-data-r2np-vamf"
