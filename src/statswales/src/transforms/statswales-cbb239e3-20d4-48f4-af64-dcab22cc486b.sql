-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS BIGINT) AS data_values,
    "Data description" AS data_description,
    "Decile" AS decile,
    "Indicator" AS indicator,
    "Notes" AS notes
FROM "statswales-cbb239e3-20d4-48f4-af64-dcab22cc486b"
