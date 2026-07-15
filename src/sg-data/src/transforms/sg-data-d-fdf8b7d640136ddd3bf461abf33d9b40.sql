-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "co_max_8hour_mean"
FROM "sg-data-d-fdf8b7d640136ddd3bf461abf33d9b40"
