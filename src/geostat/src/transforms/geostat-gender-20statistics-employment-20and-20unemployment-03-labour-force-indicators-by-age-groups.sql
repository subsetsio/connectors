-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "age",
    "gender",
    CAST("year" AS BIGINT) AS year,
    "status",
    "value"
FROM "geostat-gender-20statistics-employment-20and-20unemployment-03-labour-force-indicators-by-age-groups"
