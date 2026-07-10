-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Aggregate rows sit alongside the components they sum: `security_class_desc` ('Total Public Debt Outstanding', 'Total Treasury Securities Outstanding'). Summing an amount column without excluding them double-counts.
SELECT
    "record_date",
    "security_class_desc",
    CAST(NULLIF("curr_mth_mil_amt", 'null') AS DOUBLE) AS curr_mth_mil_amt,
    "curr_mth_1_yr_ago_mil_amt",
    CAST(NULLIF("fy_end_1_yr_ago_mil_amt", 'null') AS BIGINT) AS fy_end_1_yr_ago_mil_amt,
    CAST(NULLIF("fy_end_2_yr_ago_mil_amt", 'null') AS BIGINT) AS fy_end_2_yr_ago_mil_amt,
    CAST(NULLIF("fy_end_3_yr_ago_mil_amt", 'null') AS BIGINT) AS fy_end_3_yr_ago_mil_amt,
    CAST(NULLIF("fy_end_4_yr_ago_mil_amt", 'null') AS BIGINT) AS fy_end_4_yr_ago_mil_amt,
    CAST(NULLIF("src_line_nbr", 'null') AS BIGINT) AS src_line_nbr,
    CAST(NULLIF("record_fiscal_year", 'null') AS BIGINT) AS record_fiscal_year,
    CAST(NULLIF("record_fiscal_quarter", 'null') AS BIGINT) AS record_fiscal_quarter,
    CAST(NULLIF("record_calendar_year", 'null') AS BIGINT) AS record_calendar_year,
    CAST(NULLIF("record_calendar_quarter", 'null') AS BIGINT) AS record_calendar_quarter,
    "record_calendar_month",
    CAST(NULLIF("record_calendar_day", 'null') AS BIGINT) AS record_calendar_day
FROM "us-treasury-fiscal-data-v1-debt-mspd-mspd-table-4"
