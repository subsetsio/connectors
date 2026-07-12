-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS BIGINT) AS data_values,
    "Data description" AS data_description,
    "Area" AS area,
    "Indicator" AS indicator,
    "Period" AS period,
    "Notes" AS notes
FROM "statswales-697e1a58-0836-4811-9213-e1811839c0c9"
