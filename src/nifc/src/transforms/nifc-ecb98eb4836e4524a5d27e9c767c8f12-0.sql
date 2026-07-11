-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "OBJECTID" AS objectid,
    "agency",
    "comments",
    "active",
    "latest",
    "firecode",
    "uniquefireidentifier",
    "localincidentidentifier",
    "complexname",
    "complexfirecode",
    "datecurrent",
    "pooresponsibleunit",
    "state",
    "incomplex",
    "perimeterdatetime",
    "mapmethod",
    "gisacres",
    "incidentname",
    "fireyear",
    "shape__Area" AS shape_area,
    "shape__Length" AS shape_length
FROM "nifc-ecb98eb4836e4524a5d27e9c767c8f12-0"
