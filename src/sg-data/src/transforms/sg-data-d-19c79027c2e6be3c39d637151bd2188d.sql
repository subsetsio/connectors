-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "quarter",
    "ec_launched_status",
    "type_of_sale",
    "units"
FROM "sg-data-d-19c79027c2e6be3c39d637151bd2188d"
