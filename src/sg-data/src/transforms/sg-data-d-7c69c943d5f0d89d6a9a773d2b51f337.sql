-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "quarter",
    "type_of_sale",
    "sale_status",
    "units"
FROM "sg-data-d-7c69c943d5f0d89d6a9a773d2b51f337"
