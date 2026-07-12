-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS BIGINT) AS data_values,
    "Data description" AS data_description,
    "School" AS school,
    "Ethnic Background" AS ethnic_background,
    "Notes" AS notes
FROM "statswales-4c96d2a8-1d47-4ba1-825c-f700575b080d"
