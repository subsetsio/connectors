-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS DOUBLE) AS data_values,
    "Data description" AS data_description,
    "Year" AS year,
    "Subject" AS subject,
    "Sex" AS sex,
    "FSM" AS fsm,
    "Notes" AS notes
FROM "statswales-8573088d-58b2-4727-8a20-ed87a7a37cb2"
