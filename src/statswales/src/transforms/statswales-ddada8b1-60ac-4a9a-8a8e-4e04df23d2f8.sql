-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS BIGINT) AS data_values,
    "Data description" AS data_description,
    "Year" AS year,
    "Company Name" AS company_name,
    "Rates" AS rates,
    "Notes" AS notes
FROM "statswales-ddada8b1-60ac-4a9a-8a8e-4e04df23d2f8"
