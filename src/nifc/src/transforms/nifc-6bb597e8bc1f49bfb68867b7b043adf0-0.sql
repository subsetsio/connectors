-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "OBJECTID" AS objectid,
    "GeometryID" AS geometryid,
    "Jurisdiction" AS jurisdiction,
    "FrequencyID" AS frequencyid,
    "State" AS state,
    "MapMethod" AS mapmethod,
    "DateCurrent" AS datecurrent,
    "Comments" AS comments,
    "GlobalID" AS globalid,
    "Shape__Area" AS shape_area,
    "Shape__Length" AS shape_length
FROM "nifc-6bb597e8bc1f49bfb68867b7b043adf0-0"
