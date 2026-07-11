-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "OBJECTID" AS objectid,
    "agency",
    "comments",
    "latest",
    "gisacres",
    "incidentname",
    "localincidentidentifier",
    "state",
    "pooresponsibleunit",
    "perimeterdatetime",
    "incomplex",
    "fireyear",
    "uniquefireidentifier",
    "active",
    "complexname",
    "mapmethod",
    "shape__Area" AS shape_area,
    "shape__Length" AS shape_length
FROM "nifc-003d6c8ad1624132aa43815ab7b74ba9-0"
