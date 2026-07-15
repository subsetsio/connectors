-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Wide source table with many measured attributes or category columns; avoid summing across columns without checking the upstream definition.
SELECT
    "Number" AS number,
    "Total_Total" AS total_total,
    "Total_Males" AS total_males,
    "Total_Females" AS total_females,
    "Pre_Primary_Total" AS pre_primary_total,
    "Pre_Primary_Males" AS pre_primary_males,
    "Pre_Primary_Females" AS pre_primary_females,
    "Primary_Total" AS primary_total,
    "Primary_Males" AS primary_males,
    "Primary_Females" AS primary_females,
    "Secondary_Total" AS secondary_total,
    "Secondary_Males" AS secondary_males,
    "Secondary_Females" AS secondary_females,
    "Post_Secondary_Non_Tertiary_Total" AS post_secondary_non_tertiary_total,
    "Post_Secondary_Non_Tertiary_Males" AS post_secondary_non_tertiary_males,
    "Post_Secondary_Non_Tertiary_Females" AS post_secondary_non_tertiary_females,
    "PolytechnicDiploma_Total" AS polytechnicdiploma_total,
    "PolytechnicDiploma_Males" AS polytechnicdiploma_males,
    "PolytechnicDiploma_Females" AS polytechnicdiploma_females,
    "ProfessionalQualificationandOtherDiploma_Total" AS professionalqualificationandotherdiploma_total,
    "ProfessionalQualificationandOtherDiploma_Males" AS professionalqualificationandotherdiploma_males,
    "ProfessionalQualificationandOtherDiploma_Females" AS professionalqualificationandotherdiploma_females,
    "University_Total" AS university_total,
    "University_Males" AS university_males,
    "University_Females" AS university_females
FROM "sg-data-d-c68fe4c0be031500875ce9e3074c5cef"
