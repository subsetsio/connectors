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
    "Type of vehicle" AS type_of_vehicle,
    "Time of day" AS time_of_day,
    "Day of the week" AS day_of_the_week,
    "By highways agency" AS by_highways_agency,
    "Notes" AS notes
FROM "statswales-f82f55a2-cbad-4c44-b2a9-a0ff4fb29191"
