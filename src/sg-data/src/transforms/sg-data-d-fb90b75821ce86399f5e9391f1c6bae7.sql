-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Number" AS number,
    "Total" AS total,
    "NoQualification" AS noqualification,
    "Primary" AS primary,
    "LowerSecondary" AS lowersecondary,
    "Secondary" AS secondary,
    "UpperSecondary" AS uppersecondary,
    "Polytechnic" AS polytechnic,
    "OtherDiploma" AS otherdiploma,
    "University" AS university,
    "Students" AS students
FROM "sg-data-d-fb90b75821ce86399f5e9391f1c6bae7"
