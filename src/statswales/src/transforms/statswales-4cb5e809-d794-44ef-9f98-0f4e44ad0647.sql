-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS BIGINT) AS data_values,
    "Data description" AS data_description,
    "Type of payment" AS type_of_payment,
    "Month" AS month,
    "Area" AS area,
    "Notes" AS notes
FROM "statswales-4cb5e809-d794-44ef-9f98-0f4e44ad0647"
