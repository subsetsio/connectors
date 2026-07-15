-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS DOUBLE) AS data_values,
    "Data description" AS data_description,
    "Row" AS row,
    "Column" AS financial_category,
    "Year" AS year,
    "Authority" AS authority,
    "Notes" AS notes
FROM "statswales-c696855c-2139-4f34-8463-78899be3288d"
