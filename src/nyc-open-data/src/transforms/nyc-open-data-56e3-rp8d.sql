-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "license_number",
    "_name" AS name,
    "address",
    "city",
    "state",
    "zip",
    "phone",
    "_type" AS type,
    "status",
    "date",
    "time"
FROM "nyc-open-data-56e3-rp8d"
