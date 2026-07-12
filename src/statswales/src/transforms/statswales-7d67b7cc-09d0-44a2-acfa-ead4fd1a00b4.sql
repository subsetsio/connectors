-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS DOUBLE) AS data_values,
    "Data description" AS data_description,
    "Type of payment" AS type_of_payment,
    "Month" AS month,
    "Age" AS age,
    "Notes" AS notes
FROM "statswales-7d67b7cc-09d0-44a2-acfa-ead4fd1a00b4"
