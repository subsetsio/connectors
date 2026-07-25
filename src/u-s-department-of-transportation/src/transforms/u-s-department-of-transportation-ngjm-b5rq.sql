-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "port",
    "commodity",
    CAST("time" AS BIGINT) AS time,
    CAST("customs_containerized_vessel" AS BIGINT) AS customs_containerized_vessel,
    CAST("containerized_vessel_swt" AS BIGINT) AS containerized_vessel_swt,
    CAST("containerized_vessel_total" AS BIGINT) AS containerized_vessel_total
FROM "u-s-department-of-transportation-ngjm-b5rq"
