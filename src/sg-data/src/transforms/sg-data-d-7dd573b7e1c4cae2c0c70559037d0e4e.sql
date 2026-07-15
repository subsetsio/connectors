-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Number" AS number,
    "Total" AS total,
    "Pre_Primary" AS pre_primary,
    "Primary" AS primary,
    "Secondary" AS secondary,
    "Post_Secondary_Non_Tertiary" AS post_secondary_non_tertiary,
    "Polytechnic" AS polytechnic,
    "ProfessionalQualificationAndOtherDiploma" AS professionalqualificationandotherdiploma,
    "University" AS university
FROM "sg-data-d-7dd573b7e1c4cae2c0c70559037d0e4e"
