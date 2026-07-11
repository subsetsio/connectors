-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "OBJECTID" AS objectid,
    "active",
    "latest",
    "incidentname",
    "complexname",
    "pooresponsibleunit",
    "uniquefireidentifier",
    "gisacres",
    "perimeterdatetime",
    "comments",
    "localincidentidentifier",
    "state",
    "mapmethod",
    "datecurrent",
    "fireyear",
    "incomplex",
    "shape__Area" AS shape_area,
    "shape__Length" AS shape_length
FROM "nifc-dffc3c4f66c34ec48dbfa58041600ca5-0"
