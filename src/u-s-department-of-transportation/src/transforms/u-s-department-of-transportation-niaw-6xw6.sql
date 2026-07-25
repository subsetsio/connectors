-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("year" AS BIGINT) AS year,
    "month",
    CAST("vmt" AS BIGINT) AS vmt,
    CAST("_12_month_average" AS BIGINT) AS 12_month_average,
    CAST("vmt_cumulative" AS BIGINT) AS vmt_cumulative,
    CAST("ajd_vmt" AS BIGINT) AS ajd_vmt
FROM "u-s-department-of-transportation-niaw-6xw6"
