-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Aggregate rows sit alongside the components they sum: `type` ('Total'). Summing an amount column without excluding them double-counts.
SELECT
    "record_date",
    "type",
    CAST(NULLIF("public_prin_borrowings_amt", 'null') AS DOUBLE) AS public_prin_borrowings_amt,
    CAST(NULLIF("public_prin_repayments_amt", 'null') AS DOUBLE) AS public_prin_repayments_amt,
    CAST(NULLIF("public_interest_accrued_amt", 'null') AS DOUBLE) AS public_interest_accrued_amt,
    CAST(NULLIF("public_interest_paid_amt", 'null') AS DOUBLE) AS public_interest_paid_amt,
    CAST(NULLIF("public_net_unamortized_amt", 'null') AS DOUBLE) AS public_net_unamortized_amt,
    CAST(NULLIF("public_net_amortization_amt", 'null') AS DOUBLE) AS public_net_amortization_amt,
    CAST(NULLIF("intragov_prin_net_increase_amt", 'null') AS DOUBLE) AS intragov_prin_net_increase_amt,
    CAST(NULLIF("intragov_interest_accrued_amt", 'null') AS DOUBLE) AS intragov_interest_accrued_amt,
    CAST(NULLIF("intragov_interest_paid_amt", 'null') AS DOUBLE) AS intragov_interest_paid_amt,
    CAST(NULLIF("intragov_net_unamortized_amt", 'null') AS DOUBLE) AS intragov_net_unamortized_amt,
    CAST(NULLIF("intragov_net_amortization_amt", 'null') AS DOUBLE) AS intragov_net_amortization_amt,
    CAST(NULLIF("src_line_nbr", 'null') AS BIGINT) AS src_line_nbr,
    CAST(NULLIF("record_fiscal_year", 'null') AS BIGINT) AS record_fiscal_year,
    CAST(NULLIF("record_fiscal_quarter", 'null') AS BIGINT) AS record_fiscal_quarter,
    CAST(NULLIF("record_calendar_year", 'null') AS BIGINT) AS record_calendar_year,
    CAST(NULLIF("record_calendar_quarter", 'null') AS BIGINT) AS record_calendar_quarter,
    "record_calendar_month",
    "record_calendar_day"
FROM "us-treasury-fiscal-data-v1-accounting-od-schedules-fed-debt-daily-activity"
