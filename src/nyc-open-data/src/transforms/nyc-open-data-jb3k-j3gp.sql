-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "license_number",
    "_name" AS name,
    "_type" AS type,
    "expiration_date",
    "last_date_updated",
    "last_time_updated"
FROM "nyc-open-data-jb3k-j3gp"
