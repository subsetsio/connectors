-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "financial_year",
    "dwelling_type",
    "no_of_units"
FROM "sg-data-d-caa8f8f91cb000f4b2c4a52fd22d516c"
