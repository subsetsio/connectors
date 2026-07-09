-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "country",
    CAST("country_code" AS BIGINT) AS country_code,
    "item",
    CAST("item_code" AS BIGINT) AS item_code,
    "unit",
    "frequency",
    "date",
    "value"
FROM "afdb-dhujbpg"
