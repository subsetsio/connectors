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
    "pooresponsibleunit",
    "uniquefireidentifier",
    "localincidentidentifier",
    "incidentname",
    "inciwebid",
    "gisacres",
    "perimeterdatetime",
    "datecurrent",
    "fireyear",
    "mapmethod",
    "complexname",
    "complexfirecode",
    "incomplex",
    "state",
    "shape__Area" AS shape_area,
    "shape__Length" AS shape_length
FROM "nifc-671f7337371d430baad822d017cfef87-0"
