-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "quarter",
    CAST("year" AS BIGINT) AS year,
    "groups",
    "value"
FROM "geostat-price-20statistics-ppi-unit-20value-20index-20of-20agricultural-20products-agro-ppi-previous-quarter-100"
