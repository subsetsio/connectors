-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS DOUBLE) AS data_values,
    "Data description" AS data_description,
    strptime("Date", '%d/%m/%Y')::DATE AS date,
    "Method" AS method,
    CAST("Deprivation quintile" AS BIGINT) AS deprivation_quintile,
    "Notes" AS notes
FROM "statswales-2a9e2850-978f-4bb0-af63-e87cf8a45081"
