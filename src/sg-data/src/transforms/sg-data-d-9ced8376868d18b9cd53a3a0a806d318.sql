-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "status",
    "sex",
    "no_of_inhalant_abusers_arrested"
FROM "sg-data-d-9ced8376868d18b9cd53a3a0a806d318"
