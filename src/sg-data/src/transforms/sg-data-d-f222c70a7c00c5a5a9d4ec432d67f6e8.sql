-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "wbt_date",
    "wbt_time",
    "wet_bulb_temperature"
FROM "sg-data-d-f222c70a7c00c5a5a9d4ec432d67f6e8"
