-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "quarter",
    "type_of_sale",
    "sale_status",
    "units"
FROM "sg-data-d-5785799d63a9da091f4e0b456291eeb8"
