-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS DOUBLE) AS data_values,
    "Data description" AS data_description,
    strptime("Year ending", '%d/%m/%Y')::DATE AS year_ending,
    "Area" AS area,
    "Ethnicity" AS ethnicity,
    "Notes" AS notes
FROM "statswales-a453c250-8d77-48fc-9e97-2341c899ba5e"
