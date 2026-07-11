-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "objectid",
    "agency",
    "comments",
    "active",
    "mapmethod",
    "datecurrent",
    "uniquefireidentifier",
    "fireyear",
    "incidentname",
    "pooownerunit",
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
    "mergeid",
    "latest",
    "modifiedon",
    "createdon",
    "shape__Area" AS shape_area,
    "shape__Length" AS shape_length
FROM "nifc-a829aefbe4e5471490d8f3d47ca5410d-0"
