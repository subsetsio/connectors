-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "number_of_vessels",
    "gross_tonnage"
FROM "sg-data-d-8392e9bea6ca351a38f67172ccdf6a6a"
