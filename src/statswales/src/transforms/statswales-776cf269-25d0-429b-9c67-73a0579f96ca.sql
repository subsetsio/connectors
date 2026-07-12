-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS DOUBLE) AS data_values,
    "Data description" AS data_description,
    strptime("Date", '%d/%m/%Y')::DATE AS date,
    "Area" AS area,
    "Register" AS register,
    "Age Band" AS age_band,
    "Gender" AS gender,
    "Notes" AS notes
FROM "statswales-776cf269-25d0-429b-9c67-73a0579f96ca"
