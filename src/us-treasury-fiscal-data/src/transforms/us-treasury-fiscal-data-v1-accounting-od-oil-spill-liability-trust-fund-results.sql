-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Aggregate rows sit alongside the components they sum: `account_desc` ('Total expenditure/non-expenditure transfers'); `component_desc` ('Total expenditure/non-expenditure transfers', 'Total investment income', 'Total nonexpenditure transfers', …). Summing an amount column without excluding them double-counts.
SELECT
    "record_date",
    CAST(NULLIF("fiscal_year", 'null') AS BIGINT) AS fiscal_year,
    "table_nbr",
    "table_nm",
    "account_desc",
    "component_desc",
    "fiscal_year_amt",
    CAST(NULLIF("src_line_nbr", 'null') AS BIGINT) AS src_line_nbr,
    CAST(NULLIF("record_fiscal_year", 'null') AS BIGINT) AS record_fiscal_year,
    CAST(NULLIF("record_fiscal_quarter", 'null') AS BIGINT) AS record_fiscal_quarter,
    CAST(NULLIF("record_calendar_year", 'null') AS BIGINT) AS record_calendar_year,
    CAST(NULLIF("record_calendar_quarter", 'null') AS BIGINT) AS record_calendar_quarter,
    "record_calendar_month",
    "record_calendar_day"
FROM "us-treasury-fiscal-data-v1-accounting-od-oil-spill-liability-trust-fund-results"
