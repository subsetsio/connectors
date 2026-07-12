-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS BIGINT) AS data_values,
    "Data description" AS data_description,
    "Type of employment" AS type_of_employment,
    "Time period" AS time_period,
    "Notes" AS notes
FROM "statswales-8e99b9ce-8dc3-4aac-b5aa-b560f72cae08"
