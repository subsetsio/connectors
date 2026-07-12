-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS BIGINT) AS data_values,
    "Data description" AS data_description,
    "Financial year" AS financial_year,
    "Road classification" AS road_classification,
    "Skid resistance" AS skid_resistance,
    "Notes" AS notes
FROM "statswales-eb556d04-b067-4a5d-81dc-c8ad036b71dc"
