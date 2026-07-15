-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "quarter",
    "volume_of_mobile_data"
FROM "sg-data-d-8bf1863458eefb925c88bda1d2d30ff9"
