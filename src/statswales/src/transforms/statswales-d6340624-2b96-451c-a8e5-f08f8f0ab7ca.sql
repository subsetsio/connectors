-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS BIGINT) AS data_values,
    "Data description" AS data_description,
    "Age" AS age,
    "Contract type" AS contract_type,
    "Gender" AS gender,
    "Dental staff type" AS dental_staff_type,
    "Year" AS year,
    "Area" AS area,
    "Notes" AS notes
FROM "statswales-d6340624-2b96-451c-a8e5-f08f8f0ab7ca"
