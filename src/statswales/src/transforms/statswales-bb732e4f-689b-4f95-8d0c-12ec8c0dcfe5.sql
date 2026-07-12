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
FROM "statswales-bb732e4f-689b-4f95-8d0c-12ec8c0dcfe5"
