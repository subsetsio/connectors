-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "YEAR" AS year,
    "ICD_MAIN_CATEGORY" AS icd_main_category,
    "ICD_DETAILED_CATEGORY" AS icd_detailed_category,
    "GENDER" AS gender,
    "DEATH_AGE" AS death_age,
    "DEATH_COUNT" AS death_count
FROM "sg-data-d-716c31ea00d7c05d43d4109d8b0db3bb"
