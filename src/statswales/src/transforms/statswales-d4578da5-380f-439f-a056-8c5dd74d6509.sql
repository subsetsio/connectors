-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS DOUBLE) AS data_values,
    "Data description" AS data_description,
    "Staff group" AS staff_group,
    "Date" AS date,
    "Organisation" AS organisation,
    "Notes" AS notes
FROM "statswales-d4578da5-380f-439f-a056-8c5dd74d6509"
