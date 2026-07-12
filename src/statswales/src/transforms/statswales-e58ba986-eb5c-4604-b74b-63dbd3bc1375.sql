-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS BIGINT) AS data_values,
    "Data description" AS data_description,
    "Enrolment type" AS enrolment_type,
    "Academic year (HESA definition)" AS academic_year_hesa_definition,
    "Mode of study" AS mode_of_study,
    "Sex" AS sex,
    "Permanent address" AS permanent_address,
    "Welsh speaker status" AS welsh_speaker_status,
    "Bilingual teacher training status" AS bilingual_teacher_training_status,
    "Secondary school subject specialism" AS secondary_school_subject_specialism,
    "Notes" AS notes
FROM "statswales-e58ba986-eb5c-4604-b74b-63dbd3bc1375"
