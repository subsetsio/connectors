-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS BIGINT) AS data_values,
    "Data description" AS data_description,
    "Family type" AS family_type,
    "Time period" AS time_period,
    "Notes" AS notes
FROM "statswales-40ddfa33-9ba8-4278-ac27-1f1b0bc5fc0f"
