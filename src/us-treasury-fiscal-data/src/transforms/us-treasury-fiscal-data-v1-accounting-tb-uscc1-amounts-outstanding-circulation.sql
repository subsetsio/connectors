-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "record_date",
    "currency_coins_as_of_date",
    "currency_coins_category_desc",
    CAST(NULLIF("total_currency_coins_amt", 'null') AS BIGINT) AS total_currency_coins_amt,
    CAST(NULLIF("total_currency_amt", 'null') AS BIGINT) AS total_currency_amt,
    CAST(NULLIF("federal_reserve_notes_amt", 'null') AS BIGINT) AS federal_reserve_notes_amt,
    CAST(NULLIF("us_notes_amt", 'null') AS BIGINT) AS us_notes_amt,
    CAST(NULLIF("currency_no_longer_issued_amt", 'null') AS BIGINT) AS currency_no_longer_issued_amt,
    CAST(NULLIF("total_coins_amt", 'null') AS BIGINT) AS total_coins_amt,
    CAST(NULLIF("dollar_coins_amt", 'null') AS BIGINT) AS dollar_coins_amt,
    CAST(NULLIF("fractional_coins_amt", 'null') AS BIGINT) AS fractional_coins_amt,
    CAST(NULLIF("src_line_nbr", 'null') AS BIGINT) AS src_line_nbr,
    CAST(NULLIF("record_fiscal_year", 'null') AS BIGINT) AS record_fiscal_year,
    CAST(NULLIF("record_fiscal_quarter", 'null') AS BIGINT) AS record_fiscal_quarter,
    CAST(NULLIF("record_calendar_year", 'null') AS BIGINT) AS record_calendar_year,
    CAST(NULLIF("record_calendar_quarter", 'null') AS BIGINT) AS record_calendar_quarter,
    "record_calendar_month",
    "record_calendar_day"
FROM "us-treasury-fiscal-data-v1-accounting-tb-uscc1-amounts-outstanding-circulation"
