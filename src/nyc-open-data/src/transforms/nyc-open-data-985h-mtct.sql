-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "date",
    "fwc_monthly_eligibility_rate",
    "af_monthly_eligibility_rate"
FROM "nyc-open-data-985h-mtct"
