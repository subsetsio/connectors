-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS DOUBLE) AS data_values,
    "Data description" AS data_description,
    "Period" AS period,
    "Tax rate" AS tax_rate,
    "Notes" AS notes
FROM "statswales-5426e22f-7de4-446c-a264-60331abe6b58"
