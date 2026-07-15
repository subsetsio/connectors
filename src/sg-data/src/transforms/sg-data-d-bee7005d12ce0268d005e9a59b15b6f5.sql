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
    "Post_Secondary_Non_Tertiary" AS post_secondary_non_tertiary,
    "PolytechnicDiploma" AS polytechnicdiploma,
    "ProfessionalQualificationandOtherDiploma" AS professionalqualificationandotherdiploma,
    "University" AS university
FROM "sg-data-d-bee7005d12ce0268d005e9a59b15b6f5"
