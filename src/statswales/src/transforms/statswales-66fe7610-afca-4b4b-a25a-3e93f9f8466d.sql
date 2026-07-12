-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS BIGINT) AS data_values,
    "Data description" AS data_description,
    "Year" AS year,
    "Local Authority" AS local_authority,
    "Need category" AS need_category,
    "Disability" AS disability,
    "Notes" AS notes
FROM "statswales-66fe7610-afca-4b4b-a25a-3e93f9f8466d"
