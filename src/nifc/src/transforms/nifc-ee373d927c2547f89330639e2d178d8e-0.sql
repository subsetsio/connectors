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
    "uniquefireidentifier",
    "complexname",
    "gisacres",
    "perimeterdatetime",
    "incidentname",
    "fireyear",
    "mapmethod",
    "datecurrent",
    "pooresponsibleunit",
    "firecode",
    "localincidentidentifier",
    CAST("inciwebid" AS BIGINT) AS inciwebid,
    "incomplex",
    "state",
    "complexfirecode",
    "shape__Area" AS shape_area,
    "shape__Length" AS shape_length
FROM "nifc-ee373d927c2547f89330639e2d178d8e-0"
