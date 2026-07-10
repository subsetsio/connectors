-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "disasterNumber" AS disasternumber,
    "declarationDate" AS declarationdate,
    "fipsStateCode" AS fipsstatecode,
    "fipsCountyCode" AS fipscountycode,
    CAST("placeCode" AS BIGINT) AS placecode,
    "region",
    "stateAbbreviation" AS stateabbreviation,
    "county",
    "city",
    "damagedZipCode" AS damagedzipcode,
    "highRiskPropertyType" AS highriskpropertytype,
    "residenceType" AS residencetype,
    "floodInsurance" AS floodinsurance,
    "destroyed",
    "foundationType" AS foundationtype,
    "waterLevel" AS waterlevel,
    "highWaterLocation" AS highwaterlocation,
    "floodDamage" AS flooddamage,
    "numberOfLosses" AS numberoflosses,
    "latitude",
    "longitude",
    "id"
FROM "fema-individualassistancemultiplelossfloodproperties"
