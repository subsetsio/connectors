-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Aggregate rows sit alongside the components they sum: `classification_desc` ('Total Outlays', 'Total Receipts'). Summing an amount column without excluding them double-counts.
SELECT
    "record_date",
    "parent_id",
    CAST(NULLIF("classification_id", 'null') AS BIGINT) AS classification_id,
    "classification_desc",
    "current_month_rcpt_outly_amt",
    "current_fytd_rcpt_outly_amt",
    "prior_fytd_rcpt_outly_amt",
    "current_year_budget_est_amt",
    CAST(NULLIF("table_nbr", 'null') AS BIGINT) AS table_nbr,
    CAST(NULLIF("src_line_nbr", 'null') AS BIGINT) AS src_line_nbr,
    CAST(NULLIF("print_order_nbr", 'null') AS BIGINT) AS print_order_nbr,
    CAST(NULLIF("line_code_nbr", 'null') AS BIGINT) AS line_code_nbr,
    "data_type_cd",
    "record_type_cd",
    CAST(NULLIF("sequence_level_nbr", 'null') AS BIGINT) AS sequence_level_nbr,
    "sequence_number_cd",
    CAST(NULLIF("record_fiscal_year", 'null') AS BIGINT) AS record_fiscal_year,
    CAST(NULLIF("record_fiscal_quarter", 'null') AS BIGINT) AS record_fiscal_quarter,
    CAST(NULLIF("record_calendar_year", 'null') AS BIGINT) AS record_calendar_year,
    CAST(NULLIF("record_calendar_quarter", 'null') AS BIGINT) AS record_calendar_quarter,
    "record_calendar_month",
    CAST(NULLIF("record_calendar_day", 'null') AS BIGINT) AS record_calendar_day
FROM "us-treasury-fiscal-data-v1-accounting-mts-mts-table-3"
