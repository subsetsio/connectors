-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "_year" AS year,
    "borough",
    "uhf",
    "gender",
    "age",
    "race",
    "hiv_diagnoses",
    "hiv_diagnosis_rate",
    "concurrent_diagnoses",
    "linked_to_care_within_3_months",
    "aids_diagnoses",
    "aids_diagnosis_rate",
    "plwdhi_prevalence",
    "viral_suppression",
    "deaths",
    "death_rate",
    "hivrelated_death_rate",
    "nonhivrelated_death_rate"
FROM "nyc-open-data-fju2-rdad"
