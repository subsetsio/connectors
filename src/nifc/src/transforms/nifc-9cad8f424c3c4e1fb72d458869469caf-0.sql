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
    "incidentname",
    "uniquefireidentifier",
    "pooresponsibleunit",
    "firecode",
    "complexfirecode",
    "gisacres",
    "perimeterdatetime",
    "datecurrent",
    "fireyear",
    "localincidentidentifier",
    "state",
    "incomplex",
    "mapmethod",
    "shape__Area" AS shape_area,
    "shape__Length" AS shape_length
FROM "nifc-9cad8f424c3c4e1fb72d458869469caf-0"
