-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS DOUBLE) AS data_values,
    "Data description" AS data_description,
    "Local Authority" AS local_authority,
    "Year" AS year,
    "Flying start status" AS flying_start_status,
    "PLASC status" AS plasc_status,
    "Notes" AS notes
FROM "statswales-e35760c6-69af-48e2-b5e3-8c8151de06f2"
