-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS DOUBLE) AS data_values,
    "Data description" AS data_description,
    strptime("Date", '%d/%m/%Y')::DATE AS date,
    "Joiners or leavers" AS joiners_or_leavers,
    "GP type" AS gp_type,
    "Age" AS age,
    "Sex" AS sex,
    "Notes" AS notes
FROM "statswales-92ea144c-b47b-407f-adcf-571c5d4510ac"
