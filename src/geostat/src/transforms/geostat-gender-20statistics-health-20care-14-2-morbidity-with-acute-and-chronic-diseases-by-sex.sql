-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "sex",
    CAST("year" AS BIGINT) AS year,
    "diseases",
    "value"
FROM "geostat-gender-20statistics-health-20care-14-2-morbidity-with-acute-and-chronic-diseases-by-sex"
