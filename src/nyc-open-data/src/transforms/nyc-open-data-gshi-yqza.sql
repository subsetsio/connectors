-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "jur_dist",
    "council_dist",
    "bldg",
    "org",
    "organization_name",
    "room_no",
    "_function" AS function,
    "capacity",
    "date_as_of"
FROM "nyc-open-data-gshi-yqza"
