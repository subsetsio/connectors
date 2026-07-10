-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "record_date",
    "series_cd",
    "series_desc",
    CAST(NULLIF("bonds_issued_cnt", 'null') AS BIGINT) AS bonds_issued_cnt,
    CAST(NULLIF("bonds_redeemed_cnt", 'null') AS BIGINT) AS bonds_redeemed_cnt,
    CAST(NULLIF("bonds_out_cnt", 'null') AS BIGINT) AS bonds_out_cnt,
    CAST(NULLIF("bonds_matured_cnt", 'null') AS BIGINT) AS bonds_matured_cnt,
    CAST(NULLIF("bonds_unmatured_cnt", 'null') AS BIGINT) AS bonds_unmatured_cnt,
    CAST(NULLIF("matured_redeemed_cnt", 'null') AS BIGINT) AS matured_redeemed_cnt,
    CAST(NULLIF("matured_unredeemed_cnt", 'null') AS BIGINT) AS matured_unredeemed_cnt,
    CAST(NULLIF("unmatured_redeemed_cnt", 'null') AS BIGINT) AS unmatured_redeemed_cnt,
    CAST(NULLIF("unmatured_unredeemed_cnt", 'null') AS BIGINT) AS unmatured_unredeemed_cnt,
    CAST(NULLIF("src_line_nbr", 'null') AS BIGINT) AS src_line_nbr,
    CAST(NULLIF("record_fiscal_year", 'null') AS BIGINT) AS record_fiscal_year,
    CAST(NULLIF("record_fiscal_quarter", 'null') AS BIGINT) AS record_fiscal_quarter,
    CAST(NULLIF("record_calendar_year", 'null') AS BIGINT) AS record_calendar_year,
    CAST(NULLIF("record_calendar_quarter", 'null') AS BIGINT) AS record_calendar_quarter,
    "record_calendar_month",
    CAST(NULLIF("record_calendar_day", 'null') AS BIGINT) AS record_calendar_day
FROM "us-treasury-fiscal-data-v1-accounting-od-savings-bonds-report"
