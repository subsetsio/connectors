-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS BIGINT) AS data_values,
    "Data description" AS data_description,
    "Academic year" AS academic_year,
    "Institution" AS institution,
    "Personal characteristics" AS personal_characteristics,
    "Sex" AS sex,
    "Contract type" AS contract_type,
    "Contract mode" AS contract_mode,
    "Occupation" AS occupation,
    "Notes" AS notes
FROM "statswales-30010fd2-0e54-438e-b212-de76f20a6890"
