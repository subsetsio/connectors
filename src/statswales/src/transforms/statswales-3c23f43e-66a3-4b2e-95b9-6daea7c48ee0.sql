-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS DOUBLE) AS data_values,
    "Data description" AS data_description,
    "Local Authority" AS local_authority,
    "Year" AS year,
    "Characteristics of children" AS characteristics_of_children,
    "Notes" AS notes
FROM "statswales-3c23f43e-66a3-4b2e-95b9-6daea7c48ee0"
