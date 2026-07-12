-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS DOUBLE) AS data_values,
    "Data description" AS data_description,
    "Reason" AS reason,
    "Year" AS year,
    "Notes" AS notes
FROM "statswales-0dc5145c-d5db-413e-b4b4-eba7383390e4"
