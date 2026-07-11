-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "OBJECTID" AS objectid,
    "GeometryID" AS geometryid,
    "GACCName" AS gaccname,
    "GACCUnitID" AS gaccunitid,
    "GACCAbbreviation" AS gaccabbreviation,
    "GACCLocation" AS gacclocation,
    CAST("ContactPhone" AS BIGINT) AS contactphone,
    "Comments" AS comments,
    "DateCurrent" AS datecurrent,
    "MapMethod" AS mapmethod,
    "GlobalID" AS globalid,
    "Shape__Area" AS shape_area,
    "Shape__Length" AS shape_length
FROM "nifc-614ad98bdf834c92bf92c4f0fe197903-0"
