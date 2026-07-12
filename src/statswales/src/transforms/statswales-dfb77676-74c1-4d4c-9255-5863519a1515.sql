-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS DOUBLE) AS data_values,
    "Data description" AS data_description,
    "Frequency of speaking Welsh" AS frequency_of_speaking_welsh,
    "Age" AS age,
    "Sex" AS sex,
    strptime("Year", '%d/%m/%Y')::DATE AS year,
    "Notes" AS notes
FROM "statswales-dfb77676-74c1-4d4c-9255-5863519a1515"
