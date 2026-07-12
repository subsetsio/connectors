-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS BIGINT) AS data_values,
    "Data description" AS data_description,
    "Ethnicity" AS ethnicity,
    "Year" AS year,
    "Notes" AS notes
FROM "statswales-3db6d854-67ca-4de3-a6e0-d441013c0575"
