-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Violation rows are multi-response observations; do not aggregate as one row per driver.
SELECT
    CAST("STATE" AS BIGINT) AS state,
    CAST("ST_CASE" AS BIGINT) AS st_case,
    CAST("VEH_NO" AS BIGINT) AS veh_no,
    CAST("MVIOLATN" AS BIGINT) AS mviolatn,
    "STATENAME" AS statename,
    "MVIOLATNNAME" AS mviolatnname,
    CAST("VIOLATION" AS BIGINT) AS violation,
    "VIOLATIONNAME" AS violationname,
    "case_year"
FROM "nhtsa-fars-violatn"
