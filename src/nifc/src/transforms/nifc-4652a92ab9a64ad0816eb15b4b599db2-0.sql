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
    "complexfirecode",
    "firecode",
    "uniquefireidentifier",
    "incidentname",
    "pooresponsibleunit",
    "datecurrent",
    "fireyear",
    "gisacres",
    "perimeterdatetime",
    "state",
    "localincidentidentifier",
    "mapmethod",
    "incomplex",
    "shape__Area" AS shape_area,
    "shape__Length" AS shape_length
FROM "nifc-4652a92ab9a64ad0816eb15b4b599db2-0"
