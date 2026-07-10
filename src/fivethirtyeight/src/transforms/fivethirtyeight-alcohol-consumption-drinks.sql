-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "country",
    "beer_servings",
    "spirit_servings",
    "wine_servings",
    "total_litres_of_pure_alcohol"
FROM "fivethirtyeight-alcohol-consumption-drinks"
