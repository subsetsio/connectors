-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Aggregate rows sit alongside the components they sum: `line_item_desc` ('Total Non-interest Spending', 'Total Receipts', 'Total non-interest spending', …). Summing an amount column without excluding them double-counts.
SELECT
    "record_date",
    "account_desc",
    "line_item_desc",
    "current_year_proj_tril_amt",
    "previous_year_proj_tril_amt",
    "proj_tril_amt_change",
    CAST(NULLIF("current_year_percent_of_gdp", 'null') AS DOUBLE) AS current_year_percent_of_gdp,
    "previous_year_percent_of_gdp",
    "percent_of_gdp_change",
    CAST(NULLIF("src_line_nbr", 'null') AS BIGINT) AS src_line_nbr,
    CAST(NULLIF("record_fiscal_year", 'null') AS BIGINT) AS record_fiscal_year,
    CAST(NULLIF("record_fiscal_quarter", 'null') AS BIGINT) AS record_fiscal_quarter,
    CAST(NULLIF("record_calendar_year", 'null') AS BIGINT) AS record_calendar_year,
    CAST(NULLIF("record_calendar_quarter", 'null') AS BIGINT) AS record_calendar_quarter,
    "record_calendar_month",
    CAST(NULLIF("record_calendar_day", 'null') AS BIGINT) AS record_calendar_day
FROM "us-treasury-fiscal-data-v1-accounting-od-long-term-projections"
