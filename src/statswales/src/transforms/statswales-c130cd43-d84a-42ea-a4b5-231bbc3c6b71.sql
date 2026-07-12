-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS BIGINT) AS data_values,
    "Data description" AS data_description,
    "Enrolment type" AS enrolment_type,
    "Academic year (HESA definition)" AS academic_year_hesa_definition,
    "Level of study or qualification" AS level_of_study_or_qualification,
    "Initial teacher education phase" AS initial_teacher_education_phase,
    "Mode of study" AS mode_of_study,
    "Sex" AS sex,
    "Personal characteristics" AS personal_characteristics,
    "Notes" AS notes
FROM "statswales-c130cd43-d84a-42ea-a4b5-231bbc3c6b71"
