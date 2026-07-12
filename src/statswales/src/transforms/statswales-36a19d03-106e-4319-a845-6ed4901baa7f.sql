-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS BIGINT) AS data_values,
    "Data description" AS data_description,
    "Tenure" AS tenure,
    "Time period" AS time_period,
    "Notes" AS notes
FROM "statswales-36a19d03-106e-4319-a845-6ed4901baa7f"
