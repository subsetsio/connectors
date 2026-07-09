-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: WPI item_code is not unique by itself in the raw observations; use item_code together with item_name and date for row identity.
SELECT
    CAST("item_code" AS BIGINT) AS item_code,
    "item_name",
    "weight",
    strptime("base_year", '%Y-%m')::DATE AS base_year,
    "date",
    "index_value"
FROM "dpiit-wpi-values"
