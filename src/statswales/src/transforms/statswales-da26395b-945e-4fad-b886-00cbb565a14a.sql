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
    "Notes" AS notes
FROM "statswales-da26395b-945e-4fad-b886-00cbb565a14a"
