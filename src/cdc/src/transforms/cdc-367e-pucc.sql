-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Time Period" AS time_period,
    "Measure Type" AS measure_type,
    "Measure" AS measure,
    "Group" AS group,
    "Subgroup" AS subgroup,
    "Estimate Type" AS estimate_type,
    CAST("Estimate" AS DOUBLE) AS estimate,
    CAST("Standard Error" AS DOUBLE) AS standard_error,
    CAST("Lower 95% CI" AS DOUBLE) AS lower_95_ci,
    CAST("Upper 95% CI" AS DOUBLE) AS upper_95_ci,
    "Reliable" AS reliable
FROM "cdc-367e-pucc"
