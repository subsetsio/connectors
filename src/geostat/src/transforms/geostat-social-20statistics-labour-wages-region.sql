-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "quarter",
    CAST("year" AS BIGINT) AS year,
    "region",
    "value"
FROM "geostat-social-20statistics-labour-wages-region"
