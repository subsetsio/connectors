-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "record_date",
    "frn",
    "cusip",
    "original_dated_date",
    "original_issue_date",
    "maturity_date",
    CAST(NULLIF("spread", 'null') AS DOUBLE) AS spread,
    "start_of_accrual_period",
    "end_of_accrual_period",
    CAST(NULLIF("daily_index", 'null') AS DOUBLE) AS daily_index,
    CAST(NULLIF("daily_int_accrual_rate", 'null') AS DOUBLE) AS daily_int_accrual_rate,
    CAST(NULLIF("daily_accrued_int_per100", 'null') AS DOUBLE) AS daily_accrued_int_per100,
    CAST(NULLIF("accr_int_per100_pmt_period", 'null') AS DOUBLE) AS accr_int_per100_pmt_period
FROM "us-treasury-fiscal-data-v1-accounting-od-frn-daily-indexes"
