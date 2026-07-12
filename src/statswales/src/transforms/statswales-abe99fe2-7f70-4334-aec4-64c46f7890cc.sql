-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS DOUBLE) AS data_values,
    "Data description" AS data_description,
    "Local Authority" AS local_authority,
    CAST("Year" AS BIGINT) AS year,
    "Flying start status" AS flying_start_status,
    "Notes" AS notes
FROM "statswales-abe99fe2-7f70-4334-aec4-64c46f7890cc"
