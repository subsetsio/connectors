-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "shs_year",
    "elderly_pop",
    "ethnic_group",
    "percentage"
FROM "sg-data-d-1a5bb230195b27f5982682d4bb66bcb0"
