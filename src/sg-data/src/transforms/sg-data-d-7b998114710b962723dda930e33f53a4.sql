-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "father_race",
    "mother_race",
    "birth_count"
FROM "sg-data-d-7b998114710b962723dda930e33f53a4"
