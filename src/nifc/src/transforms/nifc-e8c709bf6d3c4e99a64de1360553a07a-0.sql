-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "OBJECTID" AS objectid,
    "agency",
    "comments",
    "active",
    "mapmethod",
    "datecurrent",
    "uniquefireidentifier",
    "fireyear",
    "incidentname",
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
    "latest",
    "shape__Area" AS shape_area,
    "shape__Length" AS shape_length
FROM "nifc-e8c709bf6d3c4e99a64de1360553a07a-0"
