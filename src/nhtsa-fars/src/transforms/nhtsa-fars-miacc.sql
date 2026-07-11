-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Multiple-imputation table; the A1-A10 fields are imputed values for the same crash concept, not independent observations.
SELECT
    CAST("ST_CASE" AS BIGINT) AS st_case,
    CAST("YEAR" AS BIGINT) AS year,
    CAST("A1" AS BIGINT) AS a1,
    CAST("A2" AS BIGINT) AS a2,
    CAST("A3" AS BIGINT) AS a3,
    CAST("A4" AS BIGINT) AS a4,
    CAST("A5" AS BIGINT) AS a5,
    CAST("A6" AS BIGINT) AS a6,
    CAST("A7" AS BIGINT) AS a7,
    CAST("A8" AS BIGINT) AS a8,
    CAST("A9" AS BIGINT) AS a9,
    CAST("A10" AS BIGINT) AS a10,
    "case_year"
FROM "nhtsa-fars-miacc"
