-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "borough_name",
    "block",
    "lot",
    "propertyzip",
    "permitnumber",
    "issuancedate",
    "applicationtype",
    "requeststatus"
FROM "nyc-open-data-hphy-6g7m"
