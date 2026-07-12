-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS DOUBLE) AS data_values,
    "Data description" AS data_description,
    strptime("12 months ending", '%d/%m/%Y')::DATE AS 12_months_ending,
    "Area" AS area,
    "Notes" AS notes
FROM "statswales-6e533581-3be9-4f8f-8fb9-3abfca467742"
