-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Number" AS number,
    "Others_Total" AS others_total,
    "Others_Pre_Primary" AS others_pre_primary,
    "Others_Primary" AS others_primary,
    "Others_Secondary" AS others_secondary,
    "Others_Post_Secondary_Non_Tertiary" AS others_post_secondary_non_tertiary,
    "Others_PolytechnicDiploma" AS others_polytechnicdiploma,
    "Others_ProfessionalQualificationandOtherDiploma" AS others_professionalqualificationandotherdiploma,
    "Others_University" AS others_university
FROM "sg-data-d-a61cdf9d3e5534912b85f3380d209272"
