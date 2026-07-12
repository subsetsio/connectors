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
    "Permanent address" AS permanent_address,
    "Welsh speaker status" AS welsh_speaker_status,
    "Bilingual teacher training status" AS bilingual_teacher_training_status,
    "Notes" AS notes
FROM "statswales-2fa702d4-8b58-4139-a259-5b674a3164eb"
