-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Vehicle sequence-of-events rows are ordered event observations; use the event number fields when reconstructing order.
SELECT
    CAST("STATE" AS BIGINT) AS state,
    CAST("ST_CASE" AS BIGINT) AS st_case,
    CAST("VEH_NO" AS BIGINT) AS veh_no,
    CAST("VEVENTNUM" AS BIGINT) AS veventnum,
    CAST("SOE" AS BIGINT) AS soe,
    CAST("AOI" AS BIGINT) AS aoi,
    "STATENAME" AS statename,
    "SOENAME" AS soename,
    "AOINAME" AS aoiname,
    "case_year"
FROM "nhtsa-fars-vsoe"
