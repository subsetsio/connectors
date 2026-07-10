-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Geographic Label" AS geographic_label,
    "Indicator Variable" AS indicator_variable,
    "Indicator Category" AS indicator_category,
    CAST("Estimate" AS DOUBLE) AS estimate,
    "95% Confidence Interval" AS 95_confidence_interval,
    CAST("Sample Size" AS BIGINT) AS sample_size,
    CAST("Suppressed Flag" AS BIGINT) AS suppressed_flag,
    "Timeframe" AS timeframe
FROM "cdc-7nbz-eajm"
