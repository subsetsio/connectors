-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS DOUBLE) AS data_values,
    "Data description" AS data_description,
    "Year" AS year,
    "Flying start status" AS flying_start_status,
    "Local Authority" AS local_authority,
    "Notes" AS notes
FROM "statswales-4da5ddfb-f57c-42f3-954c-4dd31353f598"
