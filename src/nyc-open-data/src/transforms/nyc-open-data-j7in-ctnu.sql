-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "check_number",
    strptime("check_date", '%m/%d/%Y')::DATE AS check_date,
    "bbl",
    "case_number",
    strptime("period_begin", '%m/%d/%Y')::DATE AS period_begin,
    strptime("period_end", '%m/%d/%Y')::DATE AS period_end,
    "refund_amount"
FROM "nyc-open-data-j7in-ctnu"
