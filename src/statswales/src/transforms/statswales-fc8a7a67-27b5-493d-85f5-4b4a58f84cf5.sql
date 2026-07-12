-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS BIGINT) AS data_values,
    "Data description" AS data_description,
    "Year" AS year,
    "Asylum Seeker" AS asylum_seeker,
    "Gender" AS gender,
    "Notes" AS notes
FROM "statswales-fc8a7a67-27b5-493d-85f5-4b4a58f84cf5"
