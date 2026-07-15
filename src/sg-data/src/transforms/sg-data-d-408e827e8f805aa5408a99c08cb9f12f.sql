-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Number" AS number,
    "Indians_Total" AS indians_total,
    "Indians_NoQualification" AS indians_noqualification,
    "Indians_Primary" AS indians_primary,
    "Indians_LowerSecondary" AS indians_lowersecondary,
    "Indians_Secondary" AS indians_secondary,
    "Indians_Post_Secondary_Non_Tertiary" AS indians_post_secondary_non_tertiary,
    "Indians_PolytechnicDiploma" AS indians_polytechnicdiploma,
    "Indians_ProfessionalQualificationandOtherDiploma" AS indians_professionalqualificationandotherdiploma,
    "Indians_University" AS indians_university
FROM "sg-data-d-408e827e8f805aa5408a99c08cb9f12f"
