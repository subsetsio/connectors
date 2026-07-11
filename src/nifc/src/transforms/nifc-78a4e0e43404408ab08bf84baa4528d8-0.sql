-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "OBJECTID" AS objectid,
    "GACCName" AS gaccname,
    "GACCUnitID" AS gaccunitid,
    "GACCAbbreviation" AS gaccabbreviation,
    "DispName" AS dispname,
    "DispUnitID" AS dispunitid,
    "DispLocation" AS displocation,
    "DispArea" AS disparea,
    CAST("ContactPhone" AS BIGINT) AS contactphone,
    "Comments" AS comments,
    "MapMethod" AS mapmethod,
    "GlobalID" AS globalid,
    "Shape__Area" AS shape_area,
    "Shape__Length" AS shape_length
FROM "nifc-78a4e0e43404408ab08bf84baa4528d8-0"
