-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("sysid" AS BIGINT) AS sysid,
    "sysname",
    CAST("year" AS DOUBLE) AS year,
    CAST("assigned_month" AS DOUBLE) AS assigned_month,
    CAST("yr_mo_d" AS TIMESTAMP) AS yr_mo_d,
    CAST("sum_min" AS DOUBLE) AS sum_min,
    CAST("num_trip" AS DOUBLE) AS num_trip,
    "sysname_alt"
FROM "u-s-department-of-transportation-g3h6-334u"
