-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS DOUBLE) AS data_values,
    "Data description" AS data_description,
    "Population" AS population,
    "Age" AS age,
    "Sex" AS sex,
    strptime("Year", '%d/%m/%Y')::DATE AS year,
    "Notes" AS notes
FROM "statswales-1d289a5d-f2e5-4e51-bc34-0d86558ad332"
