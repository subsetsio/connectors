-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "month",
    "rh_extremes_minimum"
FROM "sg-data-d-54445baa32ffe4d46f5bef168c4e0538"
