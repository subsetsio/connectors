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
    "Number of vehicles involved" AS number_of_vehicles_involved,
    "Notes" AS notes
FROM "statswales-50ac7e7c-18ae-4bb9-85d7-f395359e0ca3"
