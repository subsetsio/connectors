-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("OKTMO_code" AS BIGINT) AS oktmo_code,
    "OKTMO_description" AS oktmo_description,
    CAST("population" AS BIGINT) AS population,
    CAST("men" AS BIGINT) AS men,
    CAST("women" AS BIGINT) AS women,
    "urban_population",
    "urban_men_population",
    "urban_women_population",
    "rural_population",
    "rural_men_population",
    "rural_women_population"
FROM "rosstat-7708234640-population2010"
