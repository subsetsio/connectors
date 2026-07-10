-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "record_date",
    "security_type",
    "security_term",
    "first_auc_date_single_price",
    CAST(NULLIF("low_rate_pct", 'null') AS DOUBLE) AS low_rate_pct,
    "first_auc_date_low_rate",
    CAST(NULLIF("high_rate_pct", 'null') AS DOUBLE) AS high_rate_pct,
    "first_auc_date_high_rate",
    CAST(NULLIF("high_offer_amt", 'null') AS BIGINT) AS high_offer_amt,
    "first_auc_date_high_offer",
    CAST(NULLIF("high_bid_cover_ratio", 'null') AS DOUBLE) AS high_bid_cover_ratio,
    "first_auc_date_high_bid_cover",
    CAST(NULLIF("src_line_nbr", 'null') AS BIGINT) AS src_line_nbr,
    CAST(NULLIF("record_fiscal_year", 'null') AS BIGINT) AS record_fiscal_year,
    CAST(NULLIF("record_fiscal_quarter", 'null') AS BIGINT) AS record_fiscal_quarter,
    CAST(NULLIF("record_calendar_year", 'null') AS BIGINT) AS record_calendar_year,
    CAST(NULLIF("record_calendar_quarter", 'null') AS BIGINT) AS record_calendar_quarter,
    "record_calendar_month",
    "record_calendar_day"
FROM "us-treasury-fiscal-data-v2-accounting-od-record-setting-auction"
