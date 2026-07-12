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
    "Caring responsibilities" AS caring_responsibilities,
    "Notes" AS notes
FROM "statswales-1fa06532-b3b9-45da-b111-d55e4ddb6ca2"
