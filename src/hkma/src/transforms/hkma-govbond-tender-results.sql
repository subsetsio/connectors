-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "issue_number",
    "ni_ro",
    "issue_date",
    "expected_maturity_date",
    "coupon",
    "average_yield_accepted",
    "amount_applied",
    "amount_allotted",
    "bid-to-cover_ratio" AS bid_to_cover_ratio,
    "segment"
FROM "hkma-govbond-tender-results"
