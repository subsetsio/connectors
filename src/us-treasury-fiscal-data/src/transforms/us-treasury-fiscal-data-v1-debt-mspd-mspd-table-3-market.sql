-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Aggregate rows sit alongside the components they sum: `security_class1_desc` ('Total Marketable'); `security_class2_desc` ('Total Matured Treasury Bills', 'Total Matured Treasury Bonds', 'Total Matured Treasury Floating Rate Notes', …). Summing an amount column without excluding them double-counts.
SELECT
    "record_date",
    "security_type_desc",
    "security_class1_desc",
    "security_class2_desc",
    "series_cd",
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
    CAST(NULLIF("src_line_nbr", 'null') AS BIGINT) AS src_line_nbr,
    CAST(NULLIF("record_fiscal_year", 'null') AS BIGINT) AS record_fiscal_year,
    CAST(NULLIF("record_fiscal_quarter", 'null') AS BIGINT) AS record_fiscal_quarter,
    CAST(NULLIF("record_calendar_year", 'null') AS BIGINT) AS record_calendar_year,
    CAST(NULLIF("record_calendar_quarter", 'null') AS BIGINT) AS record_calendar_quarter,
    "record_calendar_month",
    CAST(NULLIF("record_calendar_day", 'null') AS BIGINT) AS record_calendar_day
FROM "us-treasury-fiscal-data-v1-debt-mspd-mspd-table-3-market"
