-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "record_date",
    "function_desc",
    "sub_function_desc",
    CAST(NULLIF("current_month_outly_amt", 'null') AS DOUBLE) AS current_month_outly_amt,
    CAST(NULLIF("current_fytd_outly_amt", 'null') AS DOUBLE) AS current_fytd_outly_amt,
    CAST(NULLIF("prior_fytd_outly_amt", 'null') AS DOUBLE) AS prior_fytd_outly_amt,
    "table_nbr",
    CAST(NULLIF("src_line_nbr", 'null') AS BIGINT) AS src_line_nbr,
    CAST(NULLIF("print_order_nbr", 'null') AS BIGINT) AS print_order_nbr,
    CAST(NULLIF("line_code_nbr", 'null') AS BIGINT) AS line_code_nbr,
    CAST(NULLIF("sequence_number_cd", 'null') AS DOUBLE) AS sequence_number_cd,
    CAST(NULLIF("record_fiscal_year", 'null') AS BIGINT) AS record_fiscal_year,
    CAST(NULLIF("record_fiscal_quarter", 'null') AS BIGINT) AS record_fiscal_quarter,
    CAST(NULLIF("record_calendar_year", 'null') AS BIGINT) AS record_calendar_year,
    CAST(NULLIF("record_calendar_quarter", 'null') AS BIGINT) AS record_calendar_quarter,
    "record_calendar_month",
    CAST(NULLIF("record_calendar_day", 'null') AS BIGINT) AS record_calendar_day
FROM "us-treasury-fiscal-data-v1-accounting-mts-mts-table-9-outlays-functions-subfunctions"
