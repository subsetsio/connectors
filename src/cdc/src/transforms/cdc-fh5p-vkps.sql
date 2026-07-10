-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("metricyear" AS BIGINT) AS metricyear,
    CAST("WeekNum" AS BIGINT) AS weeknum,
    CAST("pageviews" AS BIGINT) AS pageviews,
    "visits"
FROM "cdc-fh5p-vkps"
