-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Thousands" AS thousands,
    "Total_Total" AS total_total,
    "Total_Males" AS total_males,
    "Total_Females" AS total_females,
    "SecondaryAndBelow_Total" AS secondaryandbelow_total,
    "SecondaryAndBelow_Males" AS secondaryandbelow_males,
    "SecondaryAndBelow_Females" AS secondaryandbelow_females,
    "Post_Secondary_Non_Tertiary_Total" AS post_secondary_non_tertiary_total,
    "Post_Secondary_Non_Tertiary_Males" AS post_secondary_non_tertiary_males,
    "Post_Secondary_Non_Tertiary_Females" AS post_secondary_non_tertiary_females,
    "Polytechnic_Total" AS polytechnic_total,
    "Polytechnic_Males" AS polytechnic_males,
    "Polytechnic_Females" AS polytechnic_females,
    "ProfessionalQualificationAndOtherDiploma_Total" AS professionalqualificationandotherdiploma_total,
    "ProfessionalQualificationAndOtherDiploma_Males" AS professionalqualificationandotherdiploma_males,
    "ProfessionalQualificationAndOtherDiploma_Females" AS professionalqualificationandotherdiploma_females,
    "University_Total" AS university_total,
    "University_Males" AS university_males,
    "University_Females" AS university_females
FROM "sg-data-d-1863a2f5bba877a9cc28f61fff7ccb1f"
