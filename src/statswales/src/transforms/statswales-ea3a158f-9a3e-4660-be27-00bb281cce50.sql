-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS DOUBLE) AS data_values,
    "Data description" AS data_description,
    strptime("Date", '%d/%m/%Y')::DATE AS date,
    "Joiners or leavers" AS joiners_or_leavers,
    "Staff" AS staff,
    "Age" AS age,
    "Sex" AS sex,
    "Notes" AS notes
FROM "statswales-ea3a158f-9a3e-4660-be27-00bb281cce50"
