-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "requestid",
    "applicationid",
    "requesttype",
    "house",
    "street",
    "borough",
    "bin",
    "block",
    "lot",
    "ownername",
    "expirationdate",
    "make",
    "model",
    "burnermake",
    "burnermodel",
    "primaryfuel",
    "secondaryfuel",
    "quantity",
    "issuedate",
    "status",
    "premisename"
FROM "nyc-open-data-f4rp-2kvy"
