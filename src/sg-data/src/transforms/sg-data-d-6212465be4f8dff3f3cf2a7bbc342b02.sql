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
    "University" AS university
FROM "sg-data-d-6212465be4f8dff3f3cf2a7bbc342b02"
