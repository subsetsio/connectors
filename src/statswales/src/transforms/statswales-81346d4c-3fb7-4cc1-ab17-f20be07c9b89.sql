-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS BIGINT) AS data_values,
    "Data description" AS data_description,
    "Local authority" AS local_authority,
    "Type of licence" AS type_of_licence,
    CAST("Year" AS BIGINT) AS year,
    "Notes" AS notes
FROM "statswales-81346d4c-3fb7-4cc1-ab17-f20be07c9b89"
