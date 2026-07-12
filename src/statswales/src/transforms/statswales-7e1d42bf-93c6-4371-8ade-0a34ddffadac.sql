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
    "Type of Vehicle" AS type_of_vehicle,
    "Weather conditions" AS weather_conditions,
    "By highways agency" AS by_highways_agency,
    "Notes" AS notes
FROM "statswales-7e1d42bf-93c6-4371-8ade-0a34ddffadac"
