-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: This table is the UK inflation-adjusted series; use nominal HPI tables when comparing to unadjusted house prices.
SELECT
    "date",
    "period_label",
    "category",
    "measure",
    "value"
FROM "nationwide-hpi-uk-house-prices-adjusted-for-inflation"
