-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Aggregate rows sit alongside the components they sum: `classification_desc` ('Total Receipts Offset Against Outlays'). Summing an amount column without excluding them double-counts.
SELECT
    "record_date",
    CAST(NULLIF("classification_id", 'null') AS BIGINT) AS classification_id,
    "classification_desc",
    CAST(NULLIF("curr_fytd_rcpt_offset_amt", 'null') AS DOUBLE) AS curr_fytd_rcpt_offset_amt,
    CAST(NULLIF("prior_fytd_rcpt_offset_amt", 'null') AS DOUBLE) AS prior_fytd_rcpt_offset_amt,
    "table_nbr",
    CAST(NULLIF("src_line_nbr", 'null') AS BIGINT) AS src_line_nbr,
    CAST(NULLIF("print_order_nbr", 'null') AS BIGINT) AS print_order_nbr,
    CAST(NULLIF("line_code_nbr", 'null') AS BIGINT) AS line_code_nbr,
    "data_type_cd",
    "record_type_cd",
    CAST(NULLIF("sequence_level_nbr", 'null') AS BIGINT) AS sequence_level_nbr,
    CAST(NULLIF("sequence_number_cd", 'null') AS BIGINT) AS sequence_number_cd,
    CAST(NULLIF("record_fiscal_year", 'null') AS BIGINT) AS record_fiscal_year,
    CAST(NULLIF("record_fiscal_quarter", 'null') AS BIGINT) AS record_fiscal_quarter,
    CAST(NULLIF("record_calendar_year", 'null') AS BIGINT) AS record_calendar_year,
    CAST(NULLIF("record_calendar_quarter", 'null') AS BIGINT) AS record_calendar_quarter,
    "record_calendar_month",
    CAST(NULLIF("record_calendar_day", 'null') AS BIGINT) AS record_calendar_day
FROM "us-treasury-fiscal-data-v1-accounting-mts-mts-table-5m"
