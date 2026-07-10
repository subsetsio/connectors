-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "record_date",
    "parent_id",
    CAST(NULLIF("classification_id", 'null') AS BIGINT) AS classification_id,
    "classification_desc",
    "current_month_gross_rcpt_amt",
    "current_month_gross_outly_amt",
    "current_month_dfct_sur_amt",
    CAST(NULLIF("table_nbr", 'null') AS BIGINT) AS table_nbr,
    CAST(NULLIF("src_line_nbr", 'null') AS BIGINT) AS src_line_nbr,
    CAST(NULLIF("print_order_nbr", 'null') AS BIGINT) AS print_order_nbr,
    CAST(NULLIF("line_code_nbr", 'null') AS BIGINT) AS line_code_nbr,
    "data_type_cd",
    "record_type_cd",
    CAST(NULLIF("sequence_level_nbr", 'null') AS BIGINT) AS sequence_level_nbr,
    CAST(NULLIF("sequence_number_cd", 'null') AS DOUBLE) AS sequence_number_cd,
    CAST(NULLIF("record_fiscal_year", 'null') AS BIGINT) AS record_fiscal_year,
    CAST(NULLIF("record_fiscal_quarter", 'null') AS BIGINT) AS record_fiscal_quarter,
    CAST(NULLIF("record_calendar_year", 'null') AS BIGINT) AS record_calendar_year,
    CAST(NULLIF("record_calendar_quarter", 'null') AS BIGINT) AS record_calendar_quarter,
    "record_calendar_month",
    CAST(NULLIF("record_calendar_day", 'null') AS BIGINT) AS record_calendar_day
FROM "us-treasury-fiscal-data-v1-accounting-mts-mts-table-1"
