-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("STATE" AS BIGINT) AS state,
    CAST("ST_CASE" AS BIGINT) AS st_case,
    CAST("EVENTNUM" AS BIGINT) AS eventnum,
    CAST("VEH_NO" AS BIGINT) AS veh_no,
    CAST("VEVENTNUM" AS BIGINT) AS veventnum,
    CAST("VNUMBER1" AS BIGINT) AS vnumber1,
    CAST("AOI1" AS BIGINT) AS aoi1,
    CAST("SOE" AS BIGINT) AS soe,
    CAST("VNUMBER2" AS BIGINT) AS vnumber2,
    CAST("AOI2" AS BIGINT) AS aoi2,
    "STATENAME" AS statename,
    "AOI1NAME" AS aoi1name,
    "SOENAME" AS soename,
    "VNUMBER2NAME" AS vnumber2name,
    "AOI2NAME" AS aoi2name,
    "case_year"
FROM "nhtsa-fars-vevent"
