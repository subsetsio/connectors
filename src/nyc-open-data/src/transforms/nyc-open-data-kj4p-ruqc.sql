-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "buildingid",
    "boroid",
    "boro",
    "housenumber",
    "lowhousenumber",
    "highhousenumber",
    "streetname",
    "zip",
    "block",
    "lot",
    "bin",
    "communityboard",
    "censustract",
    "managementprogram",
    "dobbuildingclassid",
    "dobbuildingclass",
    "legalstories",
    "legalclassa",
    "legalclassb",
    "registrationid",
    "lifecycle",
    "recordstatusid",
    "recordstatus"
FROM "nyc-open-data-kj4p-ruqc"
