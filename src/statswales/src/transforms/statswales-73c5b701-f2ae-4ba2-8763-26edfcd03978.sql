-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS DOUBLE) AS data_values,
    "Data description" AS data_description,
    "Year" AS year,
    "Local authority" AS local_authority,
    "Year group" AS year_group,
    "Notes" AS notes
FROM "statswales-73c5b701-f2ae-4ba2-8763-26edfcd03978"
