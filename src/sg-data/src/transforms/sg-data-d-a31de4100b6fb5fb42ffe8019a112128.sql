-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Number" AS number,
    "Malays_Total" AS malays_total,
    "Malays_NoQualification" AS malays_noqualification,
    "Malays_Primary" AS malays_primary,
    "Malays_LowerSecondary" AS malays_lowersecondary,
    "Malays_Secondary" AS malays_secondary,
    "Malays_Post_Secondary_Non_Tertiary" AS malays_post_secondary_non_tertiary,
    "Malays_PolytechnicDiploma" AS malays_polytechnicdiploma,
    "Malays_ProfessionalQualificationandOtherDiploma" AS malays_professionalqualificationandotherdiploma,
    "Malays_University" AS malays_university
FROM "sg-data-d-a31de4100b6fb5fb42ffe8019a112128"
