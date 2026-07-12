-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS DOUBLE) AS data_values,
    "Data description" AS data_description,
    "Measure" AS measure,
    strptime("24 months ending", '%d/%m/%Y')::DATE AS 24_months_ending,
    "Area" AS area,
    "Notes" AS notes
FROM "statswales-dba5d285-3177-451e-bacf-6aa2788c4282"
