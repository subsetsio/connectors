-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Indicator" AS indicator,
    "Group" AS group,
    "State" AS state,
    "Subgroup" AS subgroup,
    "Phase" AS phase,
    CAST("Time Period" AS BIGINT) AS time_period,
    "Time Period Label" AS time_period_label,
    strptime("Time Period Start Date", '%m/%d/%Y')::DATE AS time_period_start_date,
    strptime("Time Period End Date", '%m/%d/%Y')::DATE AS time_period_end_date,
    CAST("Value" AS DOUBLE) AS value,
    CAST("Low CI" AS DOUBLE) AS low_ci,
    CAST("High CI" AS DOUBLE) AS high_ci,
    "Confidence Interval" AS confidence_interval,
    "Quartile Range" AS quartile_range
FROM "cdc-xb3p-q62w"
