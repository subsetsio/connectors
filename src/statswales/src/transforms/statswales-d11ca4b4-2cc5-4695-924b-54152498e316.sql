-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS DOUBLE) AS data_values,
    "Data description" AS data_description,
    "Population" AS population,
    "Local Authority" AS local_authority,
    strptime("Year", '%d/%m/%Y')::DATE AS year,
    "Notes" AS notes
FROM "statswales-d11ca4b4-2cc5-4695-924b-54152498e316"
