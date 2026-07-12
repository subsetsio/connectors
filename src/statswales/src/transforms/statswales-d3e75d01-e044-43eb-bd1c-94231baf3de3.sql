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
FROM "statswales-d3e75d01-e044-43eb-bd1c-94231baf3de3"
