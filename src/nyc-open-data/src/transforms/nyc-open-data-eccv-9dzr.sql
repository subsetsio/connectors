-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "license_number",
    "entity_name",
    "telephone_number",
    "shl_endorsed",
    "building",
    "street",
    "city",
    "state",
    "postcode",
    "type_of_base",
    "latitude",
    "longitude",
    "date",
    "time",
    "_location" AS location
FROM "nyc-open-data-eccv-9dzr"
