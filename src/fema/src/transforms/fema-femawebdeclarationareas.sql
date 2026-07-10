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
    "designatedDate" AS designateddate,
    "entryDate" AS entrydate,
    "updateDate" AS updatedate,
    "closeoutDate" AS closeoutdate,
    "lastRefresh" AS lastrefresh,
    "hash"
FROM "fema-femawebdeclarationareas"
