-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Indicator" AS indicator,
    "Group" AS group,
    "State" AS state,
    "Subgroup" AS subgroup,
    CAST("Phase" AS DOUBLE) AS phase,
    CAST("Time Period" AS BIGINT) AS time_period,
    "Time Period Label" AS time_period_label,
    strptime("Time Period Start Date", '%m/%d/%Y')::DATE AS time_period_start_date,
    strptime("Time Period End Date", '%m/%d/%Y')::DATE AS time_period_end_date,
    CAST("Value" AS DOUBLE) AS value,
    CAST("LowCI" AS DOUBLE) AS lowci,
    CAST("HighCI" AS DOUBLE) AS highci,
    "Confidence Interval" AS confidence_interval,
    "Quartile range" AS quartile_range,
    CAST("Quartile number" AS BIGINT) AS quartile_number,
    CAST("Suppression Flag" AS BIGINT) AS suppression_flag
FROM "cdc-gsea-w83j"
