-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS BIGINT) AS data_values,
    "Data description" AS data_description,
    "Year" AS year,
    "Local Authority" AS local_authority,
    "Area Code" AS area_code,
    "Child Status" AS child_status,
    "Notes" AS notes
FROM "statswales-25ec8faa-b3f8-404b-9bb5-a89fef88b54c"
