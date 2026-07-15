-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "sgd_per_unit_of_usd"
FROM "sg-data-d-6cb7c12d5f25f0a04e70657dfebcb514"
