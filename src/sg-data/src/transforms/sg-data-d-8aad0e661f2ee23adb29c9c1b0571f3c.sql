-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "quarter",
    "industry",
    "overtime_paid_hours"
FROM "sg-data-d-8aad0e661f2ee23adb29c9c1b0571f3c"
