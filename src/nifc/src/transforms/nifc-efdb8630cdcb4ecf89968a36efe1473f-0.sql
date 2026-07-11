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
    "incidentname",
    "fireyear",
    "firecode",
    "uniquefireidentifier",
    "datecurrent",
    "pooresponsibleunit",
    "complexname",
    "complexfirecode",
    "perimeterdatetime",
    "gisacres",
    "mapmethod",
    "localincidentidentifier",
    "incomplex",
    "state",
    "shape__Area" AS shape_area,
    "shape__Length" AS shape_length
FROM "nifc-efdb8630cdcb4ecf89968a36efe1473f-0"
