-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Multiple-imputation table; the P1-P10 fields are imputed values for the same person concept, not independent observations.
SELECT
    CAST("ST_CASE" AS BIGINT) AS st_case,
    CAST("VEH_NO" AS BIGINT) AS veh_no,
    CAST("PER_NO" AS BIGINT) AS per_no,
    CAST("YEAR" AS BIGINT) AS year,
    CAST("P1" AS BIGINT) AS p1,
    CAST("P2" AS BIGINT) AS p2,
    CAST("P3" AS BIGINT) AS p3,
    CAST("P4" AS BIGINT) AS p4,
    CAST("P5" AS BIGINT) AS p5,
    CAST("P6" AS BIGINT) AS p6,
    CAST("P7" AS BIGINT) AS p7,
    CAST("P8" AS BIGINT) AS p8,
    CAST("P9" AS BIGINT) AS p9,
    CAST("P10" AS BIGINT) AS p10,
    "case_year"
FROM "nhtsa-fars-miper"
