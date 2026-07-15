-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "shs_year",
    "flat_type",
    "economically_active_status",
    "no"
FROM "sg-data-d-bdc3b0ce289a7f95309b82454cf2c366"
