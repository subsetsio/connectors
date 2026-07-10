-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Aggregate rows sit alongside the components they sum: `currency_denom` ('Total Currency'). Summing an amount column without excluding them double-counts.
SELECT
    "record_date",
    "currency_as_of_date",
    "currency_denom",
    CAST(NULLIF("total_currency_amt", 'null') AS BIGINT) AS total_currency_amt,
    CAST(NULLIF("federal_reserve_notes_amt", 'null') AS BIGINT) AS federal_reserve_notes_amt,
    CAST(NULLIF("us_notes_amt", 'null') AS BIGINT) AS us_notes_amt,
    CAST(NULLIF("currency_no_longer_issued_amt", 'null') AS BIGINT) AS currency_no_longer_issued_amt,
    CAST(NULLIF("per_capita_amt", 'null') AS BIGINT) AS per_capita_amt,
    CAST(NULLIF("src_line_nbr", 'null') AS BIGINT) AS src_line_nbr,
    CAST(NULLIF("record_fiscal_year", 'null') AS BIGINT) AS record_fiscal_year,
    CAST(NULLIF("record_fiscal_quarter", 'null') AS BIGINT) AS record_fiscal_quarter,
    CAST(NULLIF("record_calendar_year", 'null') AS BIGINT) AS record_calendar_year,
    CAST(NULLIF("record_calendar_quarter", 'null') AS BIGINT) AS record_calendar_quarter,
    "record_calendar_month",
    "record_calendar_day"
FROM "us-treasury-fiscal-data-v1-accounting-tb-uscc2-amounts-outstanding-circulation"
