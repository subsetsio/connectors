-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "hijrah_year",
    "number_of_pilgrims"
FROM "sg-data-d-7100046f24d7bec79118dc027adb9f5e"
