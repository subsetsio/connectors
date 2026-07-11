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
    "complexname",
    "uniquefireidentifier",
    "complexfirecode",
    "firecode",
    "localincidentidentifier",
    "pooresponsibleunit",
    "gisacres",
    "datecurrent",
    "state",
    "incomplex",
    "mapmethod",
    "perimeterdatetime",
    "incidentname",
    "fireyear",
    "shape__Area" AS shape_area,
    "shape__Length" AS shape_length
FROM "nifc-fe9a015608f04d4aa614548a6afa6dd8-0"
