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
    "mapmethod",
    "complexfirecode",
    "incidentname",
    "uniquefireidentifier",
    "firecode",
    "localincidentidentifier",
    "datecurrent",
    "perimeterdatetime",
    "incomplex",
    "fireyear",
    "gisacres",
    "inciwebid",
    "pooresponsibleunit",
    "state",
    "shape__Area" AS shape_area,
    "shape__Length" AS shape_length
FROM "nifc-fe3e824f60254901b9408143870769fb-0"
