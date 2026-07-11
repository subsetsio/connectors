-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("year" AS BIGINT) AS year,
    "number_of_issued_restrictive_orders",
    "value"
FROM "geostat-gender-20statistics-crime-07-number-of-issued-restrictive-orders"
