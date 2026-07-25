-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "id",
    CAST("year" AS BIGINT) AS year,
    CAST("date" AS TIMESTAMP) AS date,
    CAST("value" AS DOUBLE) AS value,
    "measure",
    CAST("measurenum" AS BIGINT) AS measurenum,
    "metric",
    CAST("metricnum" AS BIGINT) AS metricnum,
    CAST("table" AS BIGINT) AS table,
    "notes",
    "source"
FROM "u-s-department-of-transportation-h2kz-rw8a"
