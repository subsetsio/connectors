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
FROM "sg-data-d-b09978b03689cc3e057d8e30145d96db"
