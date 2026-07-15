-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "month",
    "vehicle_type",
    "number"
FROM "sg-data-d-2ecb009f1e1ec5a816a454944dec4022"
