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
    "mapmethod",
    "complexname",
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
FROM "nifc-9fd76e1a84934a8997777d7fbd7ed293-0"
