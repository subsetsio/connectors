-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Thousands" AS thousands,
    "Total" AS total,
    "NoQualification" AS noqualification,
    "Primary" AS primary,
    "LowerSecondary" AS lowersecondary,
    "Secondary" AS secondary,
    "Post_Secondary_Non_Tertiary" AS post_secondary_non_tertiary,
    "Polytechnic" AS polytechnic,
    "ProfessionalQualificationAndOtherDiploma" AS professionalqualificationandotherdiploma,
    "University" AS university
FROM "sg-data-d-6ecbd5a2ec00e6caf0950c91934b74bd"
