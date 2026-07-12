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
FROM "statswales-0aa3fbd6-b5c4-4f7e-abfd-bd42fe49237b"
