-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("year" AS BIGINT) AS year,
    CAST("value" AS DOUBLE) AS value,
    "measure",
    "metric",
    "table",
    "source",
    "notes",
    CAST("measurenum" AS BIGINT) AS measurenum,
    CAST("metricnum" AS BIGINT) AS metricnum,
    CAST("date" AS TIMESTAMP) AS date,
    "id"
FROM "u-s-department-of-transportation-tcq5-4pgu"
