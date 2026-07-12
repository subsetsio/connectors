-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS BIGINT) AS data_values,
    "Data description" AS data_description,
    "Authority" AS authority,
    "Year" AS year,
    "Exemption class" AS exemption_class,
    "Notes" AS notes
FROM "statswales-3230b0bc-f90f-4233-9d4b-5de3cdf02c84"
