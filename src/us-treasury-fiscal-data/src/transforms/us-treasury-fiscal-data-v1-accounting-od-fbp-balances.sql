-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "record_date",
    "account_nbr",
    "account_desc",
    "security_nbr",
    "segment_desc",
    CAST(NULLIF("loans_receivable_amt", 'null') AS DOUBLE) AS loans_receivable_amt,
    CAST(NULLIF("interest_receivable_amt", 'null') AS DOUBLE) AS interest_receivable_amt,
    CAST(NULLIF("capitalized_int_receivable_amt", 'null') AS DOUBLE) AS capitalized_int_receivable_amt,
    CAST(NULLIF("amortization_amt", 'null') AS DOUBLE) AS amortization_amt,
    "maturity_date",
    CAST(NULLIF("interest_rate_pct", 'null') AS DOUBLE) AS interest_rate_pct,
    CAST(NULLIF("sort_order_primary", 'null') AS BIGINT) AS sort_order_primary,
    CAST(NULLIF("sort_order_secondary", 'null') AS BIGINT) AS sort_order_secondary,
    CAST(NULLIF("record_fiscal_year", 'null') AS BIGINT) AS record_fiscal_year,
    CAST(NULLIF("record_fiscal_quarter", 'null') AS BIGINT) AS record_fiscal_quarter,
    CAST(NULLIF("record_calendar_year", 'null') AS BIGINT) AS record_calendar_year,
    CAST(NULLIF("record_calendar_quarter", 'null') AS BIGINT) AS record_calendar_quarter,
    "record_calendar_month",
    CAST(NULLIF("record_calendar_day", 'null') AS BIGINT) AS record_calendar_day
FROM "us-treasury-fiscal-data-v1-accounting-od-fbp-balances"
