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
FROM "geostat-social-20statistics-justice-data-on-dv-by-age"
