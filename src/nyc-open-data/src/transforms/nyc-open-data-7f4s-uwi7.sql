-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "election",
    "candid",
    "candname",
    "officecd",
    "officeboro",
    "officedist",
    "canclass",
    "earlypay",
    "primarypay",
    "generalpay",
    "runoffpay",
    "totalpay"
FROM "nyc-open-data-7f4s-uwi7"
