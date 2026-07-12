-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS DOUBLE) AS data_values,
    "Data description" AS data_description,
    "Year" AS year,
    "Authority" AS authority,
    "Indicator Name" AS indicator_name,
    "Notes" AS notes
FROM "statswales-3f618fb3-af31-4e61-a141-90e64703472b"
