-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "app_no",
    "_type" AS type,
    "app_date",
    "status",
    "fru_interview_scheduled",
    "drug_test",
    "wav_course",
    "defensive_driving",
    "driver_exam",
    "medical_clearance_form",
    "other_requirements",
    "last_updated"
FROM "nyc-open-data-p32s-yqxq"
