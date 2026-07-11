-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "expected_maturity_date",
    "original_maturity",
    "issue_number",
    "isin_code",
    CAST("stock_code" AS BIGINT) AS stock_code,
    "coupon",
    "outstanding_size",
    "institutional_retail"
FROM "hkma-govbond-outstanding-list"
