-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "pri_students_to_teachers"
FROM "sg-data-d-bc5a1a10afedf7d25128dae1342c9556"
