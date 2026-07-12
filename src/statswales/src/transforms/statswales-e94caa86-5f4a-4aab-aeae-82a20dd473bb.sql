-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS DOUBLE) AS data_values,
    "Data description" AS data_description,
    "Period" AS period,
    "Relief type" AS relief_type,
    "Transaction type" AS transaction_type,
    "Impact on tax" AS impact_on_tax,
    "Notes" AS notes
FROM "statswales-e94caa86-5f4a-4aab-aeae-82a20dd473bb"
