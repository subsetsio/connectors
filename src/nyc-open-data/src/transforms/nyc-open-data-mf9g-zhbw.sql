-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "address",
    "bbl",
    "bin",
    "boro",
    "borocd",
    "city",
    "c_and_d",
    "districtcode",
    "objectid",
    "_label" AS label,
    "mgp",
    "_name" AS name,
    "organics",
    "paper",
    "refuse",
    "state",
    "zip",
    "point",
    "swm_facility_id"
FROM "nyc-open-data-mf9g-zhbw"
