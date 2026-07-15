-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Number" AS number,
    "Chinese_Total" AS chinese_total,
    "Chinese_Pre_Primary" AS chinese_pre_primary,
    "Chinese_Primary" AS chinese_primary,
    "Chinese_Secondary" AS chinese_secondary,
    "Chinese_Post_Secondary_Non_Tertiary" AS chinese_post_secondary_non_tertiary,
    "Chinese_PolytechnicDiploma" AS chinese_polytechnicdiploma,
    "Chinese_ProfessionalQualificationandOtherDiploma" AS chinese_professionalqualificationandotherdiploma,
    "Chinese_University" AS chinese_university
FROM "sg-data-d-453018de40b2f290e270fb62b4c87b9b"
