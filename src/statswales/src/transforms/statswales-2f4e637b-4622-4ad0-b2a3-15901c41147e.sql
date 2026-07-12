-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS DOUBLE) AS data_values,
    "Data description" AS data_description,
    "Organisation" AS organisation,
    "Year" AS year,
    "Programme category" AS programme_category,
    "Commissioner" AS commissioner,
    "Notes" AS notes
FROM "statswales-2f4e637b-4622-4ad0-b2a3-15901c41147e"
