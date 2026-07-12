-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS DOUBLE) AS data_values,
    "Data description" AS data_description,
    "Kilometres travelled or passenger journeys" AS kilometres_travelled_or_passenger_journeys,
    "Year" AS year,
    "Notes" AS notes
FROM "statswales-9dfb7c8a-538f-4c72-b3bd-b0834213112e"
