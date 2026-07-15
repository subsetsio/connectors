-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "manpower",
    "growth"
FROM "sg-data-d-77fa870aa3afb10a1d133b20e9651b6e"
