-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "from",
    "type_of_duty",
    "type_of_bet",
    "amount_taxed_on",
    "tax_rate"
FROM "sg-data-d-2d16ccf3773d3d98b749b3381db6b60a"
