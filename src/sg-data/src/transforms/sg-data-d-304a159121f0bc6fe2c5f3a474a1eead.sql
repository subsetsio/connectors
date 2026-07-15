-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "level_1",
    "level_2",
    "value"
FROM "sg-data-d-304a159121f0bc6fe2c5f3a474a1eead"
