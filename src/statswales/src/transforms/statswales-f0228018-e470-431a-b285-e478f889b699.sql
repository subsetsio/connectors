-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS BIGINT) AS data_values,
    "Data description" AS data_description,
    "Date" AS date,
    "Area" AS area,
    "Severity" AS severity,
    "Number of casualties" AS number_of_casualties,
    "Notes" AS notes
FROM "statswales-f0228018-e470-431a-b285-e478f889b699"
