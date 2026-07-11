-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "OBJECTID" AS objectid,
    "agency",
    "comments",
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
    "shape__Area" AS shape_area,
    "shape__Length" AS shape_length
FROM "nifc-ef25d7e8c9f3499ba9e3d8e09606e488-0"
