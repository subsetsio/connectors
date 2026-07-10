-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "record_date",
    "state_nm",
    CAST(NULLIF("interest_rate_pct", 'null') AS DOUBLE) AS interest_rate_pct,
    CAST(NULLIF("outstanding_advance_bal", 'null') AS DOUBLE) AS outstanding_advance_bal,
    CAST(NULLIF("advance_auth_month_amt", 'null') AS DOUBLE) AS advance_auth_month_amt,
    CAST(NULLIF("gross_advance_draws_month_amt", 'null') AS DOUBLE) AS gross_advance_draws_month_amt,
    CAST(NULLIF("interest_accrued_fytd_amt", 'null') AS DOUBLE) AS interest_accrued_fytd_amt,
    CAST(NULLIF("interest_paid_amt", 'null') AS DOUBLE) AS interest_paid_amt,
    CAST(NULLIF("src_line_nbr", 'null') AS BIGINT) AS src_line_nbr,
    CAST(NULLIF("record_fiscal_year", 'null') AS BIGINT) AS record_fiscal_year,
    CAST(NULLIF("record_fiscal_quarter", 'null') AS BIGINT) AS record_fiscal_quarter,
    CAST(NULLIF("record_calendar_year", 'null') AS BIGINT) AS record_calendar_year,
    CAST(NULLIF("record_calendar_quarter", 'null') AS BIGINT) AS record_calendar_quarter,
    "record_calendar_month",
    "record_calendar_day"
FROM "us-treasury-fiscal-data-v2-accounting-od-title-xii"
