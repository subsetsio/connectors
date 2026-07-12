-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS BIGINT) AS data_values,
    "Data description" AS data_description,
    "Year" AS year,
    "Sector" AS sector,
    "Category" AS category,
    "Notes" AS notes
FROM "statswales-2ba6add6-fd02-4d40-909a-4ad3af881ff1"
