-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "tmc",
    CAST("day_of_week" AS BIGINT) AS day_of_week,
    CAST("time_bin" AS BIGINT) AS time_bin,
    CAST("volume" AS BIGINT) AS volume,
    CAST("percent_commercial" AS DOUBLE) AS percent_commercial
FROM "u-s-department-of-transportation-6t2m-6b8t"
