-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS BIGINT) AS data_values,
    "Data description" AS data_description,
    "Cause of injury or death" AS cause_of_injury_or_death,
    "Financial year" AS financial_year,
    "Fire and Rescue Authority area" AS fire_and_rescue_authority_area,
    "Notes" AS notes
FROM "statswales-3643d017-ff94-479b-a5ef-52a807665bce"
