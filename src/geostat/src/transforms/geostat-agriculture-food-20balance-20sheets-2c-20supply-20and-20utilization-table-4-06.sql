-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("year" AS BIGINT) AS year,
    "indicators",
    "value"
FROM "geostat-agriculture-food-20balance-20sheets-2c-20supply-20and-20utilization-table-4-06"
