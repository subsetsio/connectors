-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS BIGINT) AS data_values,
    "Data description" AS data_description,
    "Year" AS year,
    "Age" AS age,
    "Area" AS area,
    "Contract type" AS contract_type,
    "Gender" AS gender,
    "Dentist type" AS dentist_type,
    "Joiners or leavers" AS joiners_or_leavers,
    "Notes" AS notes
FROM "statswales-140e46f6-707d-4b30-8d4c-9b001196d705"
