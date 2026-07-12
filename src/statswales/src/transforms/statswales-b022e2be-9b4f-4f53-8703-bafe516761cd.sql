-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS DOUBLE) AS data_values,
    "Data description" AS data_description,
    "Period" AS period,
    "Geographical area" AS geographical_area,
    "Notes" AS notes
FROM "statswales-b022e2be-9b4f-4f53-8703-bafe516761cd"
