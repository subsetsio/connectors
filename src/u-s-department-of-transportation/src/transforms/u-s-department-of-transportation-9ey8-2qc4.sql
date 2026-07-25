-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("report_year" AS BIGINT) AS report_year,
    CAST("year" AS BIGINT) AS year,
    "item",
    "vehicle_type",
    CAST("data" AS DOUBLE) AS data
FROM "u-s-department-of-transportation-9ey8-2qc4"
