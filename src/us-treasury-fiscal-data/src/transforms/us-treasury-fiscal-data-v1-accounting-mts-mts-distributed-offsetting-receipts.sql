-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "record_date",
    CAST(NULLIF("line_cd", 'null') AS BIGINT) AS line_cd,
    "classification_desc",
    "aid_cd",
    "a_cd",
    "main_cd",
    "sub_cd",
    "betc_cd",
    CAST(NULLIF("current_month_amt", 'null') AS DOUBLE) AS current_month_amt,
    CAST(NULLIF("current_ytd_amt", 'null') AS DOUBLE) AS current_ytd_amt,
    CAST(NULLIF("src_line_nbr", 'null') AS BIGINT) AS src_line_nbr,
    CAST(NULLIF("record_fiscal_year", 'null') AS BIGINT) AS record_fiscal_year,
    CAST(NULLIF("record_fiscal_quarter", 'null') AS BIGINT) AS record_fiscal_quarter,
    CAST(NULLIF("record_calendar_year", 'null') AS BIGINT) AS record_calendar_year,
    CAST(NULLIF("record_calendar_quarter", 'null') AS BIGINT) AS record_calendar_quarter,
    "record_calendar_month",
    CAST(NULLIF("record_calendar_day", 'null') AS BIGINT) AS record_calendar_day
FROM "us-treasury-fiscal-data-v1-accounting-mts-mts-distributed-offsetting-receipts"
