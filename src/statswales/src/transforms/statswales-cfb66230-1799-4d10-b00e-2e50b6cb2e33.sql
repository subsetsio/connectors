-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS DOUBLE) AS data_values,
    "Data description" AS data_description,
    CAST("Year" AS BIGINT) AS year,
    "Area" AS area,
    "Smoking status" AS smoking_status,
    "Age of mother" AS age_of_mother,
    "Ethnic group" AS ethnic_group,
    "Indicator" AS indicator,
    "Notes" AS notes
FROM "statswales-cfb66230-1799-4d10-b00e-2e50b6cb2e33"
