-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "sector",
    "type_of_rnd_manpower",
    "fte"
FROM "sg-data-d-9bad05d1afb13f6a11c243fd65f1d0f1"
