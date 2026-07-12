-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS DOUBLE) AS data_values,
    "Data description" AS data_description,
    "Quarter" AS quarter,
    "Area" AS area,
    "Contact" AS contact,
    "Notes" AS notes
FROM "statswales-1bd6c9ef-74e5-4d5e-a525-b8470568c9b2"
