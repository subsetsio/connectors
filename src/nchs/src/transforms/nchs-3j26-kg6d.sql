-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: The source publishes this as an independent aggregate table, but no stable non-null row key was verified in the current raw profile; treat rows as source observations rather than relying on a declared unique key.
SELECT
    "figure_number",
    "setting",
    "select_measure",
    "select_measure_2",
    "response_category",
    "population",
    "value_type",
    "reporting_period",
    "select_group",
    "value",
    "low_95_ci",
    "high_95_ci",
    "reliability"
FROM "nchs-3j26-kg6d"
