-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "OBJECTID" AS objectid,
    "latest",
    "state",
    "comments",
    "incidentname",
    "complexname",
    "incomplex",
    "pooresponsibleunit",
    "gisacres",
    "fireyear",
    "uniquefireidentifier",
    "localincidentidentifier",
    "perimeterdatetime",
    "active",
    "shape__Area" AS shape_area,
    "shape__Length" AS shape_length
FROM "nifc-c0175d834e9b43e8aa0f72ca3f4eef68-0"
