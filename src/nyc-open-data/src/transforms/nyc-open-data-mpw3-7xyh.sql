-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "report_date",
    "referral_source_type",
    "total_referred",
    "total_ineligible"
FROM "nyc-open-data-mpw3-7xyh"
