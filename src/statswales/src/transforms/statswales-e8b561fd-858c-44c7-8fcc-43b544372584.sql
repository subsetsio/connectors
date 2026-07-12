-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS BIGINT) AS data_values,
    "Data description" AS data_description,
    "Year" AS year,
    "Region" AS region,
    "Tenure" AS tenure,
    "Notes" AS notes
FROM "statswales-e8b561fd-858c-44c7-8fcc-43b544372584"
