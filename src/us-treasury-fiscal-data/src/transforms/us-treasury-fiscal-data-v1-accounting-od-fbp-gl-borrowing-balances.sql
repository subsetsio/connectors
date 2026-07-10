-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Aggregate rows sit alongside the components they sum: `account_cd` ('Grand Total'). Summing an amount column without excluding them double-counts.
SELECT
    "record_date",
    "account_cd",
    "dept_cd",
    CAST(NULLIF("loans_receivable_amt", 'null') AS DOUBLE) AS loans_receivable_amt,
    "capitalized_int_receivable_amt",
    CAST(NULLIF("interest_receivable_amt", 'null') AS DOUBLE) AS interest_receivable_amt,
    CAST(NULLIF("interest_revenue_amt", 'null') AS DOUBLE) AS interest_revenue_amt,
    "gain_amt",
    "loss_amt",
    CAST(NULLIF("src_line_nbr", 'null') AS BIGINT) AS src_line_nbr,
    CAST(NULLIF("record_fiscal_year", 'null') AS BIGINT) AS record_fiscal_year,
    CAST(NULLIF("record_fiscal_quarter", 'null') AS BIGINT) AS record_fiscal_quarter,
    CAST(NULLIF("record_calendar_year", 'null') AS BIGINT) AS record_calendar_year,
    CAST(NULLIF("record_calendar_quarter", 'null') AS BIGINT) AS record_calendar_quarter,
    "record_calendar_month",
    CAST(NULLIF("record_calendar_day", 'null') AS BIGINT) AS record_calendar_day
FROM "us-treasury-fiscal-data-v1-accounting-od-fbp-gl-borrowing-balances"
