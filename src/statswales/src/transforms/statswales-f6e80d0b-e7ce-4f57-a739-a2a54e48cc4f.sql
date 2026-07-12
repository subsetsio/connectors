-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS DOUBLE) AS data_values,
    "Data description" AS data_description,
    "Effective period" AS effective_period,
    "Refund approved period" AS refund_approved_period,
    "Notes" AS notes
FROM "statswales-f6e80d0b-e7ce-4f57-a739-a2a54e48cc4f"
