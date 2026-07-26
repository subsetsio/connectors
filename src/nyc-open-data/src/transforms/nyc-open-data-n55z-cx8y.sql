-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "permitno",
    "expiration_date",
    "companyname",
    "city",
    "state",
    "zipcode",
    "issuedate",
    "permitprintdate",
    "permittype",
    "_location" AS location,
    "validdates",
    "validtimes",
    "platestate",
    "reason",
    "purpose",
    "conditionrestrictions"
FROM "nyc-open-data-n55z-cx8y"
