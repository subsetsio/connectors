-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "operation_date",
    "operation_start_time_est",
    "cusip_nbr",
    CAST(NULLIF("coupon_rate_pct", 'null') AS DOUBLE) AS coupon_rate_pct,
    "maturity_date",
    "par_amt_accepted",
    "weighted_avg_accepted_price"
FROM "us-treasury-fiscal-data-v1-accounting-od-buybacks-security-details"
