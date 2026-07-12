-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS BIGINT) AS data_values,
    "Data description" AS data_description,
    strptime("Period", '%d/%m/%Y')::DATE AS period,
    "Area" AS area,
    "Notes" AS notes
FROM "statswales-116be6b0-97bb-4abc-8cfb-13ff4b5d5d7e"
