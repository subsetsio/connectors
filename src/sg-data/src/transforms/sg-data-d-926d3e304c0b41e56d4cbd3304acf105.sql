-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "mth",
    "peak_system_demand_mw"
FROM "sg-data-d-926d3e304c0b41e56d4cbd3304acf105"
