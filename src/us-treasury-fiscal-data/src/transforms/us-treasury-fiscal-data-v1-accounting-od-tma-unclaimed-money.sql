-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Aggregate rows sit alongside the components they sum: `agency_location_cd` ('Total'); `agency_nm` ('Grand Total'). Summing an amount column without excluding them double-counts.
SELECT
    "record_date",
    "agency_nm",
    "agency_location_cd",
    CAST(NULLIF("prev_fy_end_account_bal_amt", 'null') AS DOUBLE) AS prev_fy_end_account_bal_amt,
    CAST(NULLIF("fytd_account_activity_amt", 'null') AS DOUBLE) AS fytd_account_activity_amt,
    CAST(NULLIF("account_bal_amt", 'null') AS DOUBLE) AS account_bal_amt,
    CAST(NULLIF("src_line_nbr", 'null') AS BIGINT) AS src_line_nbr,
    CAST(NULLIF("record_fiscal_year", 'null') AS BIGINT) AS record_fiscal_year,
    CAST(NULLIF("record_fiscal_quarter", 'null') AS BIGINT) AS record_fiscal_quarter,
    CAST(NULLIF("record_calendar_year", 'null') AS BIGINT) AS record_calendar_year,
    CAST(NULLIF("record_calendar_quarter", 'null') AS BIGINT) AS record_calendar_quarter,
    "record_calendar_month",
    CAST(NULLIF("record_calendar_day", 'null') AS BIGINT) AS record_calendar_day
FROM "us-treasury-fiscal-data-v1-accounting-od-tma-unclaimed-money"
