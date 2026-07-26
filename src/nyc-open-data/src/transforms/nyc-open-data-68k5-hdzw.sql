-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "recoupid",
    "sourcedescription",
    "accidentdate",
    "policereportid",
    "_location" AS location,
    "datereceived",
    "closedate",
    "status",
    "latestactiondescription",
    "borough",
    "precinctid",
    "description",
    "unitdescription",
    "companyname",
    "requestamount",
    "hasadminfee",
    "adminfee",
    "paidamount"
FROM "nyc-open-data-68k5-hdzw"
