-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Aggregate rows sit alongside the components they sum: `line_item_nm` ('Grand Total', 'Total Inflation Compensation', 'Totals'). Summing an amount column without excluding them double-counts.
SELECT
    "record_date",
    "account_number_tas",
    "account_name",
    "date_range",
    "sub_category",
    "line_item_nm",
    CAST(NULLIF("beginning_balance", 'null') AS DOUBLE) AS beginning_balance,
    CAST(NULLIF("net_change", 'null') AS DOUBLE) AS net_change,
    CAST(NULLIF("ending_balance", 'null') AS DOUBLE) AS ending_balance,
    CAST(NULLIF("src_line_nbr", 'null') AS BIGINT) AS src_line_nbr,
    CAST(NULLIF("record_fiscal_year", 'null') AS BIGINT) AS record_fiscal_year,
    CAST(NULLIF("record_fiscal_quarter", 'null') AS BIGINT) AS record_fiscal_quarter,
    CAST(NULLIF("record_calendar_year", 'null') AS BIGINT) AS record_calendar_year,
    CAST(NULLIF("record_calendar_quarter", 'null') AS BIGINT) AS record_calendar_quarter,
    "record_calendar_month",
    "record_calendar_day"
FROM "us-treasury-fiscal-data-v1-accounting-od-fip-statement-of-account-table2"
