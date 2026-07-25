-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "tmc_code",
    CAST("measurement_tstamp" AS TIMESTAMP) AS measurement_tstamp,
    CAST("speed" AS DOUBLE) AS speed,
    CAST("average_speed" AS BIGINT) AS average_speed,
    CAST("reference_speed" AS BIGINT) AS reference_speed,
    CAST("travel_time_minutes" AS DOUBLE) AS travel_time_minutes,
    CAST("confidence_score" AS DOUBLE) AS confidence_score,
    CAST("cvalue" AS DOUBLE) AS cvalue
FROM "u-s-department-of-transportation-w8r7-b5tm"
