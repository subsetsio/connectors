-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year_of_assessment",
    "income_type",
    "amount"
FROM "sg-data-d-9be6a977c945666271657d5699cfe149"
