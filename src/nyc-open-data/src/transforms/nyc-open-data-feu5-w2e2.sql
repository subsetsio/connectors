-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "registrationcontactid",
    "registrationid",
    "_type" AS type,
    "contactdescription",
    "corporationname",
    "title",
    "firstname",
    "middleinitial",
    "lastname",
    "businesshousenumber",
    "businessstreetname",
    "businessapartment",
    "businesscity",
    "businessstate",
    "businesszip"
FROM "nyc-open-data-feu5-w2e2"
