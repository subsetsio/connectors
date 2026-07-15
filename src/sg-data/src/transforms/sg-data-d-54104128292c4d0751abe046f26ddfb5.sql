-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Number" AS number,
    "Malays_Total" AS malays_total,
    "Malays_Pre_Primary" AS malays_pre_primary,
    "Malays_Primary" AS malays_primary,
    "Malays_Secondary" AS malays_secondary,
    "Malays_Post_Secondary_Non_Tertiary" AS malays_post_secondary_non_tertiary,
    "Malays_PolytechnicDiploma" AS malays_polytechnicdiploma,
    "Malays_ProfessionalQualificationandOtherDiploma" AS malays_professionalqualificationandotherdiploma,
    "Malays_University" AS malays_university
FROM "sg-data-d-54104128292c4d0751abe046f26ddfb5"
