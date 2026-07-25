-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("year" AS BIGINT) AS year,
    CAST("month" AS BIGINT) AS month,
    CAST("date" AS TIMESTAMP) AS date,
    CAST("checks" AS BIGINT) AS checks,
    CAST("market" AS BIGINT) AS market,
    CAST("segment" AS BIGINT) AS segment,
    "checks_fit",
    CAST("market_fit" AS DOUBLE) AS market_fit,
    CAST("segment_fit" AS DOUBLE) AS segment_fit
FROM "u-s-department-of-transportation-3xj5-daif"
