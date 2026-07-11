-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "sex",
    "victims_perpetrators",
    CAST("years" AS BIGINT) AS years,
    "regions",
    "value"
FROM "geostat-gender-20statistics-crime-04-1-data-on-the-victims-and-perpetrators-of-the-domestic-violence"
