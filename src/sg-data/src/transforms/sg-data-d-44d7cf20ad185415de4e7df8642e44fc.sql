-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "sector",
    "type_of_rnd_manpower",
    "headcount"
FROM "sg-data-d-44d7cf20ad185415de4e7df8642e44fc"
