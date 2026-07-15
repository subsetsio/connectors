-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "quarter",
    "type_of_sale",
    "sale_status",
    "units"
FROM "sg-data-d-1a7823f3d31e7db4b426833833762bab"
