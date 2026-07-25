-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "port",
    "commodity",
    CAST("time" AS BIGINT) AS time,
    CAST("containerized_vessel_total" AS BIGINT) AS containerized_vessel_total,
    CAST("containerized_vessel_total_1" AS BIGINT) AS containerized_vessel_total_1,
    CAST("containerized_vessel_total_2" AS BIGINT) AS containerized_vessel_total_2
FROM "u-s-department-of-transportation-vc8a-zq94"
