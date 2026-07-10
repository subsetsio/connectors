-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "record_date",
    "from_legacy_system_cnt",
    "from_legacy_system_amt",
    "from_commercial_book_entry_cnt",
    "from_commercial_book_entry_amt",
    CAST(NULLIF("total_incoming_transfers_cnt", 'null') AS BIGINT) AS total_incoming_transfers_cnt,
    CAST(NULLIF("total_incoming_transfers_amt", 'null') AS DOUBLE) AS total_incoming_transfers_amt,
    CAST(NULLIF("trans_month", 'null') AS BIGINT) AS trans_month,
    CAST(NULLIF("src_line_nbr", 'null') AS BIGINT) AS src_line_nbr,
    CAST(NULLIF("record_fiscal_year", 'null') AS BIGINT) AS record_fiscal_year,
    CAST(NULLIF("record_fiscal_quarter", 'null') AS BIGINT) AS record_fiscal_quarter,
    CAST(NULLIF("record_calendar_year", 'null') AS BIGINT) AS record_calendar_year,
    CAST(NULLIF("record_calendar_quarter", 'null') AS BIGINT) AS record_calendar_quarter,
    "record_calendar_month",
    CAST(NULLIF("record_calendar_day", 'null') AS BIGINT) AS record_calendar_day
FROM "us-treasury-fiscal-data-v1-accounting-od-securities-transfers"
