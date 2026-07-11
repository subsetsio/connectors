-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "end_of_date",
    "term",
    "issue_no",
    "yield",
    "price",
    "segment",
    "maturity",
    "coupon"
FROM "hkma-efbn-indicative-price"
