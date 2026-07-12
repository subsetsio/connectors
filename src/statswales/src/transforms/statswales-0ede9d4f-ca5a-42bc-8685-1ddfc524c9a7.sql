-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS BIGINT) AS data_values,
    "Data description" AS data_description,
    "Year" AS year,
    "Local authority" AS local_authority,
    "Age group" AS age_group,
    "Gender" AS gender,
    "Impairment" AS impairment,
    "Notes" AS notes
FROM "statswales-0ede9d4f-ca5a-42bc-8685-1ddfc524c9a7"
