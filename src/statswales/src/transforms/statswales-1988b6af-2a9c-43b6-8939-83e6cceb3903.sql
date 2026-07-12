-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS DOUBLE) AS data_values,
    "Data description" AS data_description,
    "Authority" AS authority,
    "Year" AS year,
    "Band" AS band,
    "Notes" AS notes
FROM "statswales-1988b6af-2a9c-43b6-8939-83e6cceb3903"
