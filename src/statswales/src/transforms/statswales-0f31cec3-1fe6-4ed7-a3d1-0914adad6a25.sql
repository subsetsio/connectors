-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS BIGINT) AS data_values,
    "Data description" AS data_description,
    "Fire and Rescue Authority area" AS fire_and_rescue_authority_area,
    "Financial year" AS financial_year,
    "Notes" AS notes
FROM "statswales-0f31cec3-1fe6-4ed7-a3d1-0914adad6a25"
