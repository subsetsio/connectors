-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "quarter",
    CAST("year" AS BIGINT) AS year,
    "type",
    "value"
FROM "geostat-agriculture-food-20security-20information-table-5-09"
