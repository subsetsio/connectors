-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "itemname",
    "productline",
    "itemdescription",
    "commonname",
    "quantity",
    "containersize",
    "quantityavailable"
FROM "nyc-open-data-kz4v-8ai2"
