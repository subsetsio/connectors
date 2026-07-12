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
    "Safeguarding category" AS safeguarding_category,
    "Notes" AS notes
FROM "statswales-06a95c04-2682-42d8-af7f-077e95bcb3c4"
