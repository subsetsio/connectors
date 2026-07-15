-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Number" AS number,
    "Indians_Total" AS indians_total,
    "Indians_Pre_Primary" AS indians_pre_primary,
    "Indians_Primary" AS indians_primary,
    "Indians_Secondary" AS indians_secondary,
    "Indians_Post_Secondary_Non_Tertiary" AS indians_post_secondary_non_tertiary,
    "Indians_PolytechnicDiploma" AS indians_polytechnicdiploma,
    "Indians_ProfessionalQualificationandOtherDiploma" AS indians_professionalqualificationandotherdiploma,
    "Indians_University" AS indians_university
FROM "sg-data-d-8bf813fa292a229e5390aab94829a75f"
