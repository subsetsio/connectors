-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS BIGINT) AS data_values,
    "Data description" AS data_description,
    "Year" AS year,
    "Authority" AS authority,
    "Source of funding" AS source_of_funding,
    "Notes" AS notes
FROM "statswales-33b8d404-ee3b-4d4b-85dc-0b5db4b85103"
