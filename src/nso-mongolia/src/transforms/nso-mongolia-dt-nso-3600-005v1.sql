-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Indicator" AS indicator,
    "Energy products" AS energy_products,
    CAST("Year" AS BIGINT) AS year,
    "value",
    "unit"
FROM "nso-mongolia-dt-nso-3600-005v1"
