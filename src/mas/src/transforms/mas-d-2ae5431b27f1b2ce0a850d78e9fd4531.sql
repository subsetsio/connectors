-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "data_series_id",
    "data_series",
    "period",
    "value"
FROM "mas-d-2ae5431b27f1b2ce0a850d78e9fd4531"
