-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS BIGINT) AS data_values,
    "Data description" AS data_description,
    "Date" AS date,
    "Grade" AS grade,
    "Organisation" AS organisation,
    "Notes" AS notes
FROM "statswales-74710e9d-9bcb-42ee-ade4-699083072dd0"
