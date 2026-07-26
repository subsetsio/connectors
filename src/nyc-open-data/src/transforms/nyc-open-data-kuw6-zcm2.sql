-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "vendor_name",
    "school_affiliation",
    "_month" AS month,
    "call_count"
FROM "nyc-open-data-kuw6-zcm2"
