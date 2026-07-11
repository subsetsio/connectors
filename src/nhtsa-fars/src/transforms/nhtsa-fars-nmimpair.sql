-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("STATE" AS BIGINT) AS state,
    CAST("ST_CASE" AS BIGINT) AS st_case,
    CAST("VEH_NO" AS BIGINT) AS veh_no,
    CAST("PER_NO" AS BIGINT) AS per_no,
    CAST("NMIMPAIR" AS BIGINT) AS nmimpair,
    "STATENAME" AS statename,
    "NMIMPAIRNAME" AS nmimpairname,
    "case_year"
FROM "nhtsa-fars-nmimpair"
