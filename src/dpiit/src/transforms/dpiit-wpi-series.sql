-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: WPI item_code is not unique by itself in the raw catalog; use item_code together with item_name when joining to WPI observations.
SELECT
    "item_code",
    "item_name",
    "weight",
    "base_year"
FROM "dpiit-wpi-series"
