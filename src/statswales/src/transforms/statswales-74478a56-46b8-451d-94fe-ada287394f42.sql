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
FROM "statswales-74478a56-46b8-451d-94fe-ada287394f42"
