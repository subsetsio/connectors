-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "record_date",
    "foreign_currency_desc",
    "foreign_currency_denom",
    "report_date",
    CAST(NULLIF("spot_fwd_future_purch_amt", 'null') AS BIGINT) AS spot_fwd_future_purch_amt,
    CAST(NULLIF("spot_fwd_future_sold_amt", 'null') AS BIGINT) AS spot_fwd_future_sold_amt,
    "assets_amt",
    "liabilities_amt",
    CAST(NULLIF("call_options_bought_amt", 'null') AS BIGINT) AS call_options_bought_amt,
    CAST(NULLIF("call_options_written_amt", 'null') AS BIGINT) AS call_options_written_amt,
    CAST(NULLIF("put_options_bought_amt", 'null') AS BIGINT) AS put_options_bought_amt,
    CAST(NULLIF("put_options_written_amt", 'null') AS BIGINT) AS put_options_written_amt,
    "options_net_delta_amt",
    "exchange_rate",
    CAST(NULLIF("src_line_nbr", 'null') AS BIGINT) AS src_line_nbr,
    CAST(NULLIF("record_fiscal_year", 'null') AS BIGINT) AS record_fiscal_year,
    CAST(NULLIF("record_fiscal_quarter", 'null') AS BIGINT) AS record_fiscal_quarter,
    CAST(NULLIF("record_calendar_year", 'null') AS BIGINT) AS record_calendar_year,
    CAST(NULLIF("record_calendar_quarter", 'null') AS BIGINT) AS record_calendar_quarter,
    "record_calendar_month",
    "record_calendar_day"
FROM "us-treasury-fiscal-data-v1-accounting-tb-fcp2-monthly-report-major-market-participants"
