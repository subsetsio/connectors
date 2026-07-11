-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "OBJECTID" AS objectid,
    "GeometryID" AS geometryid,
    "GACCUnitID" AS gaccunitid,
    "DispName" AS dispname,
    "DispUnitID" AS dispunitid,
    "DispAddress" AS dispaddress,
    CAST("DispTier" AS BIGINT) AS disptier,
    "DispArea" AS disparea,
    "DispContactPhone" AS dispcontactphone,
    "DispEmail" AS dispemail,
    CAST("LatWGS84" AS DOUBLE) AS latwgs84,
    CAST("LongWGS84" AS DOUBLE) AS longwgs84,
    "Comments" AS comments,
    "DateCurrent" AS datecurrent,
    "MapMethod" AS mapmethod,
    "GlobalID" AS globalid
FROM "nifc-b8793ce5b2414754b804daf783fcc34a-0"
