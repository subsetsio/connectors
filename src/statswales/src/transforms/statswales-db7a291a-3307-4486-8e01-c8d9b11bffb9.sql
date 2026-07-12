-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS DOUBLE) AS data_values,
    "Data description" AS data_description,
    "Area code" AS area_code,
    "Area name" AS area_name,
    "Indicator" AS indicator,
    "Notes" AS notes
FROM "statswales-db7a291a-3307-4486-8e01-c8d9b11bffb9"
