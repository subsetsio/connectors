-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Aggregate rows sit alongside the components they sum: `account_desc` ('Closed group - Total present value of future expenditures in excess of future revenue Future participants:', 'Open group - Total present value of future expenditures in excess of future revenue', 'Total present value of future expenditures in excess of future revenue', …); `program_desc` ('Total present value of future expenditures in excess of future revenue'). Summing an amount column without excluding them double-counts.
SELECT
    "record_date",
    "program_desc",
    "account_desc",
    "participant_grp_desc",
    CAST(NULLIF("projection_tril_amt", 'null') AS DOUBLE) AS projection_tril_amt,
    CAST(NULLIF("src_line_nbr", 'null') AS BIGINT) AS src_line_nbr,
    CAST(NULLIF("record_fiscal_year", 'null') AS BIGINT) AS record_fiscal_year,
    CAST(NULLIF("record_fiscal_quarter", 'null') AS BIGINT) AS record_fiscal_quarter,
    CAST(NULLIF("record_calendar_year", 'null') AS BIGINT) AS record_calendar_year,
    CAST(NULLIF("record_calendar_quarter", 'null') AS BIGINT) AS record_calendar_quarter,
    "record_calendar_month",
    CAST(NULLIF("record_calendar_day", 'null') AS BIGINT) AS record_calendar_day
FROM "us-treasury-fiscal-data-v1-accounting-od-social-insurance"
