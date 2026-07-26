-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "_year" AS year,
    "neighborhood",
    "raceethnicity",
    "age",
    "total_number_of_hiv_diagnoses",
    "hiv_diagnoses_per_100000_population",
    "total_number_of_concurrent_hivaids_diagnoses",
    "proportion_of_concurrent_hivaids_diagnoses_among_all_hiv_diagnoses",
    "total_number_of_aids_diagnoses",
    "aids_diagnoses_per_100000_population",
    "borough"
FROM "nyc-open-data-dxnu-p2qd"
