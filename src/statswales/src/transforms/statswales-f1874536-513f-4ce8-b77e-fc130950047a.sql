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
    "Flying Start status" AS flying_start_status,
    "Notes" AS notes
FROM "statswales-f1874536-513f-4ce8-b77e-fc130950047a"
