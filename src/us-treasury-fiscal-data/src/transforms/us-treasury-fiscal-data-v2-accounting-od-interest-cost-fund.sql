-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "record_date",
    "fund_id",
    "fund_desc",
    "cost_type_desc",
    CAST(NULLIF("net_premium_amt", 'null') AS DOUBLE) AS net_premium_amt,
    "net_discount_amt",
    "accrued_int_amt",
    "interest_paid_amt",
    "inflation_comp_amt",
    CAST(NULLIF("month_total_amt", 'null') AS DOUBLE) AS month_total_amt,
    CAST(NULLIF("fytd_total_amt", 'null') AS DOUBLE) AS fytd_total_amt,
    CAST(NULLIF("src_line_nbr", 'null') AS BIGINT) AS src_line_nbr,
    CAST(NULLIF("record_fiscal_year", 'null') AS BIGINT) AS record_fiscal_year,
    CAST(NULLIF("record_fiscal_quarter", 'null') AS BIGINT) AS record_fiscal_quarter,
    CAST(NULLIF("record_calendar_year", 'null') AS BIGINT) AS record_calendar_year,
    CAST(NULLIF("record_calendar_quarter", 'null') AS BIGINT) AS record_calendar_quarter,
    "record_calendar_month",
    CAST(NULLIF("record_calendar_day", 'null') AS BIGINT) AS record_calendar_day
FROM "us-treasury-fiscal-data-v2-accounting-od-interest-cost-fund"
