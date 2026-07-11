-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "data_series_id",
    "data_series",
    "period",
    "value"
FROM "mas-d-d4f7c9d15692b3c08aa9bc8bc56c0a72"
