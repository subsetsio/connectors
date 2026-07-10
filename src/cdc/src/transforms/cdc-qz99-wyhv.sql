-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Geography Type" AS geography_type,
    "Geography" AS geography,
    "Group Name" AS group_name,
    "Group Category" AS group_category,
    "Indicator Name" AS indicator_name,
    "Indicator Category" AS indicator_category,
    "Time Period" AS time_period,
    CAST("Year" AS BIGINT) AS year,
    "Time Type" AS time_type,
    CAST("Estimate (%)" AS DOUBLE) AS estimate,
    "95% CI (%)" AS 95_ci,
    CAST("Sample Size" AS BIGINT) AS sample_size,
    CAST("Suppression Flag" AS BIGINT) AS suppression_flag
FROM "cdc-qz99-wyhv"
