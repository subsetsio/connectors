-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year_of_assessment",
    "tax_group",
    "income_type",
    "amount"
FROM "sg-data-d-855ec3e21bba9532ca390ad8c91d422b"
