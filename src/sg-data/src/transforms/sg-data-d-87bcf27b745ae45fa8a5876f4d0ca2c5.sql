-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "contraband_cases_count"
FROM "sg-data-d-87bcf27b745ae45fa8a5876f4d0ca2c5"
