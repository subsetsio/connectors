-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS BIGINT) AS data_values,
    "Data description" AS data_description,
    "Local Authority" AS local_authority,
    "Academic year" AS academic_year,
    "Notes" AS notes
FROM "statswales-b52951f7-d1e0-4b04-9250-c983f69003f4"
