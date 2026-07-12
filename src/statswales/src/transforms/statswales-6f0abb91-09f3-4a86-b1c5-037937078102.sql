-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS DOUBLE) AS data_values,
    "Data description" AS data_description,
    "Activity" AS activity,
    "Area" AS area,
    "Date" AS date,
    "Notes" AS notes
FROM "statswales-6f0abb91-09f3-4a86-b1c5-037937078102"
