-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year_of_assessment",
    "type_of_tax_set_offs",
    "no_of_claimants",
    "amount"
FROM "sg-data-d-1ff7566f5c1ffa0e27f799b16a5ad1d9"
