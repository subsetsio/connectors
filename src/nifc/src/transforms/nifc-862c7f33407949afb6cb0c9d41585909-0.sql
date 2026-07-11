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
    "gisacres",
    "complexname",
    "incidentname",
    "pooresponsibleunit",
    "fireyear",
    "datecurrent",
    "uniquefireidentifier",
    "firecode",
    "complexfirecode",
    "localincidentidentifier",
    "perimeterdatetime",
    "mapmethod",
    "state",
    "incomplex",
    "shape__Area" AS shape_area,
    "shape__Length" AS shape_length
FROM "nifc-862c7f33407949afb6cb0c9d41585909-0"
