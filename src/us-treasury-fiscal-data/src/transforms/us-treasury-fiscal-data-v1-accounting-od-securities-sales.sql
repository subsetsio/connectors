-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "record_date",
    "security_type_desc",
    "security_class_desc",
    CAST(NULLIF("securities_sold_cnt", 'null') AS BIGINT) AS securities_sold_cnt,
    CAST(NULLIF("gross_sales_amt", 'null') AS DOUBLE) AS gross_sales_amt,
    CAST(NULLIF("returned_sales_amt", 'null') AS DOUBLE) AS returned_sales_amt,
    CAST(NULLIF("net_sales_amt", 'null') AS DOUBLE) AS net_sales_amt,
    CAST(NULLIF("trans_month", 'null') AS BIGINT) AS trans_month,
    CAST(NULLIF("src_line_nbr", 'null') AS BIGINT) AS src_line_nbr,
    CAST(NULLIF("record_fiscal_year", 'null') AS BIGINT) AS record_fiscal_year,
    CAST(NULLIF("record_fiscal_quarter", 'null') AS BIGINT) AS record_fiscal_quarter,
    CAST(NULLIF("record_calendar_year", 'null') AS BIGINT) AS record_calendar_year,
    CAST(NULLIF("record_calendar_quarter", 'null') AS BIGINT) AS record_calendar_quarter,
    "record_calendar_month",
    CAST(NULLIF("record_calendar_day", 'null') AS BIGINT) AS record_calendar_day
FROM "us-treasury-fiscal-data-v1-accounting-od-securities-sales"
