-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS BIGINT) AS data_values,
    "Data description" AS data_description,
    "Financial year" AS financial_year,
    "Month" AS month,
    "Fire and Rescue Area" AS fire_and_rescue_area,
    "Motive" AS motive,
    "Location type" AS location_type,
    "Notes" AS notes
FROM "statswales-9ab23d5a-7930-46ce-bb8d-faa4648a1097"
