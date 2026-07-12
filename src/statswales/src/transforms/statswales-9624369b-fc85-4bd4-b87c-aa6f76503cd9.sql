-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS BIGINT) AS data_values,
    "Data description" AS data_description,
    "Location type" AS location_type,
    "Fire and Rescue Authority area" AS fire_and_rescue_authority_area,
    "Motive" AS motive,
    "Financial year" AS financial_year,
    "Notes" AS notes
FROM "statswales-9624369b-fc85-4bd4-b87c-aa6f76503cd9"
