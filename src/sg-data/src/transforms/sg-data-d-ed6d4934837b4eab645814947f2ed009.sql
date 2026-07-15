-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Number" AS number,
    "Chinese_Total" AS chinese_total,
    "Chinese_NoQualification" AS chinese_noqualification,
    "Chinese_Primary" AS chinese_primary,
    "Chinese_LowerSecondary" AS chinese_lowersecondary,
    "Chinese_Secondary" AS chinese_secondary,
    "Chinese_Post_Secondary_Non_Tertiary" AS chinese_post_secondary_non_tertiary,
    "Chinese_PolytechnicDiploma" AS chinese_polytechnicdiploma,
    "Chinese_ProfessionalQualificationandOtherDiploma" AS chinese_professionalqualificationandotherdiploma,
    "Chinese_University" AS chinese_university
FROM "sg-data-d-ed6d4934837b4eab645814947f2ed009"
