-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: The source publishes this as an independent aggregate table, but no stable non-null row key was verified in the current raw profile; treat rows as source observations rather than relying on a declared unique key.
SELECT
    "indicator",
    "group",
    "state",
    "subgroup",
    "phase",
    "time_period",
    "time_period_label",
    strptime("time_period_start_date", '%m/%d/%Y')::DATE AS time_period_start_date,
    strptime("time_period_end_date", '%m/%d/%Y')::DATE AS time_period_end_date,
    "value",
    "low_ci",
    "high_ci",
    "confidence_interval",
    "quartile_range",
    "quartile_number",
    "suppression_flag"
FROM "nchs-jb9g-gnvr"
