-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "OBJECTID" AS objectid,
    "agency",
    "comments",
    "active",
    "mapmethod",
    "datecurrent",
    "uniquefireidentifier",
    "fireyear",
    "incidentname",
    "pooownerunit",
    "perimeterdatetime",
    "gisacres",
    "complexname",
    "firecode",
    "complexparentirwinid",
    "pooresponsibleunit",
    "state",
    "inciwebid",
    "localincidentidentifier",
    "irwinid",
    "incomplex",
    "complexfirecode",
    "latest",
    "shape__Area" AS shape_area,
    "shape__Length" AS shape_length
FROM "nifc-7c1b4059cc6c441297d7d2b3573cb337-0"
