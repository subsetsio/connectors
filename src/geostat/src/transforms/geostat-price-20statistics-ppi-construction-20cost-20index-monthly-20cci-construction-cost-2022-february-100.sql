-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "month",
    CAST("year" AS BIGINT) AS year,
    "groups",
    "value"
FROM "geostat-price-20statistics-ppi-construction-20cost-20index-monthly-20cci-construction-cost-2022-february-100"
