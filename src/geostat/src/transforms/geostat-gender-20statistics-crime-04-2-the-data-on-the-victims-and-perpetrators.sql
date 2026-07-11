-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "gender",
    "perpetrator_victim",
    CAST("year" AS BIGINT) AS year,
    "age",
    "region",
    "value"
FROM "geostat-gender-20statistics-crime-04-2-the-data-on-the-victims-and-perpetrators"
