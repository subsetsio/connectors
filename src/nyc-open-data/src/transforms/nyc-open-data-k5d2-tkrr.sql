-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "district",
    "disaggregation_category",
    "category",
    "total_enrollment",
    "blended",
    "blended_1",
    "remote",
    "remote_1"
FROM "nyc-open-data-k5d2-tkrr"
