-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS DOUBLE) AS data_values,
    "Data description" AS data_description,
    "Year" AS year,
    "Local Authority" AS local_authority,
    "Immunisation status" AS immunisation_status,
    "Flying start status" AS flying_start_status,
    "Notes" AS notes
FROM "statswales-f5060a7c-8b2c-41c4-985f-f0a75a5dac5f"
