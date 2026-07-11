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
    "pooresponsibleunit",
    "uniquefireidentifier",
    "fireyear",
    "firecode",
    "perimeterdatetime",
    "localincidentidentifier",
    "incidentname",
    "complexfirecode",
    "complexname",
    "incomplex",
    "mapmethod",
    "state",
    "datecurrent",
    "shape__Area" AS shape_area,
    "shape__Length" AS shape_length
FROM "nifc-13dc2b7882f645009731442e42a3ffd2-0"
