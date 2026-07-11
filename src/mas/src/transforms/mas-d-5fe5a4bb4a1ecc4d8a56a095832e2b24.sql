-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "data_series_id",
    "data_series",
    "period",
    "value"
FROM "mas-d-5fe5a4bb4a1ecc4d8a56a095832e2b24"
