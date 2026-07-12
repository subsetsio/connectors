-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS DOUBLE) AS data_values,
    "Data description" AS data_description,
    "Frequency of speaking Welsh" AS frequency_of_speaking_welsh,
    "Local Authority" AS local_authority,
    strptime("Year", '%d/%m/%Y')::DATE AS year,
    "Notes" AS notes
FROM "statswales-f66b78dd-e166-4e8e-9b61-d2a61d0c39e3"
