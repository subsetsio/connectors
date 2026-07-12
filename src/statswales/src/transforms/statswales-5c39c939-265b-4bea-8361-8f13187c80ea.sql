-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS BIGINT) AS data_values,
    "Data description" AS data_description,
    CAST("Year" AS BIGINT) AS year,
    "Area" AS area,
    "Ethnicity" AS ethnicity,
    "Welsh" AS welsh,
    "Notes" AS notes
FROM "statswales-5c39c939-265b-4bea-8361-8f13187c80ea"
