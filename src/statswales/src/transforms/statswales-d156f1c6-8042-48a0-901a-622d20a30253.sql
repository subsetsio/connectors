-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS DOUBLE) AS data_values,
    "Data description" AS data_description,
    CAST("Year" AS BIGINT) AS year,
    "Sex" AS sex,
    "Economic activity" AS economic_activity,
    "Notes" AS notes
FROM "statswales-d156f1c6-8042-48a0-901a-622d20a30253"
