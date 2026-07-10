-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "record_date",
    "auction_date",
    "issue_date",
    "securities_desc",
    "period_to_final_maturity",
    CAST(NULLIF("tendered_mil_amt", 'null') AS BIGINT) AS tendered_mil_amt,
    CAST(NULLIF("acc_mil_amt", 'null') AS BIGINT) AS acc_mil_amt,
    "acc_yield_discount_margin",
    "eq_price_for_notes_bonds",
    CAST(NULLIF("src_line_nbr", 'null') AS BIGINT) AS src_line_nbr,
    CAST(NULLIF("record_fiscal_year", 'null') AS BIGINT) AS record_fiscal_year,
    CAST(NULLIF("record_fiscal_quarter", 'null') AS BIGINT) AS record_fiscal_quarter,
    CAST(NULLIF("record_calendar_year", 'null') AS BIGINT) AS record_calendar_year,
    CAST(NULLIF("record_calendar_quarter", 'null') AS BIGINT) AS record_calendar_quarter,
    "record_calendar_month",
    "record_calendar_day"
FROM "us-treasury-fiscal-data-v1-accounting-tb-pdo2-offerings-marketable-securities-other-regular-weekly-treasury-bills"
