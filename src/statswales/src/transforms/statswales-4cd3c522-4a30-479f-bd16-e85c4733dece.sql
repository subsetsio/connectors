-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS DOUBLE) AS data_values,
    "Data description" AS data_description,
    "Period" AS period,
    "National Park area" AS national_park_area,
    "Transaction type" AS transaction_type,
    "Notes" AS notes
FROM "statswales-4cd3c522-4a30-479f-bd16-e85c4733dece"
