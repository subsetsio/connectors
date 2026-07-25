-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "id",
    "disasterNumber" AS disasternumber,
    "programTypeCode" AS programtypecode,
    "programTypeDescription" AS programtypedescription,
    "stateCode" AS statecode,
    "stateName" AS statename,
    CAST("placeCode" AS BIGINT) AS placecode,
    "placeName" AS placename,
    CASE WHEN year("designatedDate") > 2200 THEN NULL ELSE "designatedDate" END AS designateddate,
    CASE WHEN year("entryDate") > 2200 THEN NULL ELSE "entryDate" END AS entrydate,
    CASE WHEN year("updateDate") > 2200 THEN NULL ELSE "updateDate" END AS updatedate,
    CASE WHEN year("closeoutDate") > 2200 THEN NULL ELSE "closeoutDate" END AS closeoutdate,
    "lastRefresh" AS lastrefresh,
    "hash"
FROM "fema-femawebdeclarationareas"
