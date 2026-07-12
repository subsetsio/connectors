-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS BIGINT) AS data_values,
    "Data description" AS data_description,
    "Category" AS category,
    "Local Authority" AS local_authority,
    "Notes" AS notes
FROM "statswales-0a33c5ea-4263-437c-ab48-d72a03be01f9"
