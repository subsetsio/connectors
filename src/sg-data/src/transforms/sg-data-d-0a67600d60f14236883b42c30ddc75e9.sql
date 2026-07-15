-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "annual_leave_entitlement",
    "distribution"
FROM "sg-data-d-0a67600d60f14236883b42c30ddc75e9"
