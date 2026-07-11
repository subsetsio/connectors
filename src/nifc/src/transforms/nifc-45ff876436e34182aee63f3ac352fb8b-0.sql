-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "OBJECTID" AS objectid,
    "PSANAME" AS psaname,
    "GACCName" AS gaccname,
    "GACCUnitID" AS gaccunitid,
    "Comments" AS comments,
    "MapMethod" AS mapmethod,
    "PSANationalCode" AS psanationalcode,
    "DateCurrent" AS datecurrent,
    "GlobalID" AS globalid,
    "Shape__Area" AS shape_area,
    "Shape__Length" AS shape_length
FROM "nifc-45ff876436e34182aee63f3ac352fb8b-0"
