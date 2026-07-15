-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS DOUBLE) AS data_values,
    "Data description" AS data_description,
    "Year" AS year,
    "Service" AS service,
    "Column" AS financial_category,
    "Authority" AS authority,
    "Notes" AS notes
FROM "statswales-3ec7377f-0e31-421a-ab65-8a29002e1c5a"
