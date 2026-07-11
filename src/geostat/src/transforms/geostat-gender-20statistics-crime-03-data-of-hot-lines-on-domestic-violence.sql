-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "age",
    CAST("years" AS BIGINT) AS years,
    "value"
FROM "geostat-gender-20statistics-crime-03-data-of-hot-lines-on-domestic-violence"
