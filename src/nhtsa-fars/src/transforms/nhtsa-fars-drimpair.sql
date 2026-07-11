-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("STATE" AS BIGINT) AS state,
    CAST("ST_CASE" AS BIGINT) AS st_case,
    CAST("VEH_NO" AS BIGINT) AS veh_no,
    CAST("DRIMPAIR" AS BIGINT) AS drimpair,
    "STATENAME" AS statename,
    "DRIMPAIRNAME" AS drimpairname,
    "case_year"
FROM "nhtsa-fars-drimpair"
