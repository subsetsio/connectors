-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Aggregate rows sit alongside the components they sum: `security_class1_desc` ('Total Depositary Securities', 'Total Domestic Series', 'Total Foreign Series', …); `security_class2_desc` ('Total Matured State and Local Goverment Series', 'Total Matured State and Local Government Series', 'Total Matured Treasury Bills', …); `security_class3_desc` ('Total Government Account Series', 'Total Government Account Series - Held By The Public', 'Total Government Account Series - Held By the Public', …). Summing an amount column without excluding them double-counts.
SELECT
    "record_date",
    "security_type_desc",
    "series_cd",
    "security_class1_desc",
    "security_class2_desc",
    "security_class3_desc",
    "interest_rate_pct",
    "yield_pct",
    "issue_date",
    "maturity_date",
    "interest_pay_date_1",
    "interest_pay_date_2",
    "interest_pay_date_3",
    "interest_pay_date_4",
    "issued_amt",
    "inflation_adj_amt",
    "redeemed_amt",
    "outstanding_amt",
    "prior_month_outstanding_amt",
    "current_month_issued_amt",
    "current_month_redeemed_amt",
    "current_month_outstanding_amt",
    CAST(NULLIF("src_line_nbr", 'null') AS BIGINT) AS src_line_nbr,
    CAST(NULLIF("record_fiscal_year", 'null') AS BIGINT) AS record_fiscal_year,
    CAST(NULLIF("record_fiscal_quarter", 'null') AS BIGINT) AS record_fiscal_quarter,
    CAST(NULLIF("record_calendar_year", 'null') AS BIGINT) AS record_calendar_year,
    CAST(NULLIF("record_calendar_quarter", 'null') AS BIGINT) AS record_calendar_quarter,
    "record_calendar_month",
    CAST(NULLIF("record_calendar_day", 'null') AS BIGINT) AS record_calendar_day
FROM "us-treasury-fiscal-data-v1-debt-mspd-mspd-table-3"
