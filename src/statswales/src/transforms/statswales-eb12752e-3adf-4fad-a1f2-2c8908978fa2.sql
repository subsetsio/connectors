-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS DOUBLE) AS data_values,
    "Data description" AS data_description,
    "Type of vehicle" AS type_of_vehicle,
    "Year" AS year,
    "Notes" AS notes
FROM "statswales-eb12752e-3adf-4fad-a1f2-2c8908978fa2"
