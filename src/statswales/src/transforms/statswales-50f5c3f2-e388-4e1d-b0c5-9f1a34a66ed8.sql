-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS BIGINT) AS data_values,
    "Data description" AS data_description,
    "Period" AS period,
    "Area" AS area,
    "Reason" AS reason,
    "Notes" AS notes
FROM "statswales-50f5c3f2-e388-4e1d-b0c5-9f1a34a66ed8"
