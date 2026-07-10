-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "record_date",
    "tax_refund_type",
    "tax_refund_type_desc",
    CAST(NULLIF("tax_refund_today_amt", 'null') AS BIGINT) AS tax_refund_today_amt,
    CAST(NULLIF("tax_refund_mtd_amt", 'null') AS BIGINT) AS tax_refund_mtd_amt,
    CAST(NULLIF("tax_refund_fytd_amt", 'null') AS BIGINT) AS tax_refund_fytd_amt,
    "table_nbr",
    "table_nm",
    "sub_table_name",
    CAST(NULLIF("src_line_nbr", 'null') AS BIGINT) AS src_line_nbr,
    CAST(NULLIF("record_fiscal_year", 'null') AS BIGINT) AS record_fiscal_year,
    CAST(NULLIF("record_fiscal_quarter", 'null') AS BIGINT) AS record_fiscal_quarter,
    CAST(NULLIF("record_calendar_year", 'null') AS BIGINT) AS record_calendar_year,
    CAST(NULLIF("record_calendar_quarter", 'null') AS BIGINT) AS record_calendar_quarter,
    "record_calendar_month",
    "record_calendar_day"
FROM "us-treasury-fiscal-data-v1-accounting-dts-income-tax-refunds-issued"
