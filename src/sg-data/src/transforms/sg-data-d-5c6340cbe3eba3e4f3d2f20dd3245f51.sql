-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "industry",
    "overtime_paid_hours"
FROM "sg-data-d-5c6340cbe3eba3e4f3d2f20dd3245f51"
