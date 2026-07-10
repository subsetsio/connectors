-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "record_date",
    CAST(NULLIF("public_principal_mil_amt", 'null') AS DOUBLE) AS public_principal_mil_amt,
    CAST(NULLIF("public_accr_int_pay_mil_amt", 'null') AS DOUBLE) AS public_accr_int_pay_mil_amt,
    CAST(NULLIF("public_net_unamortized_mil_amt", 'null') AS DOUBLE) AS public_net_unamortized_mil_amt,
    CAST(NULLIF("intragov_principal_mil_amt", 'null') AS DOUBLE) AS intragov_principal_mil_amt,
    CAST(NULLIF("intragov_accr_int_pay_mil_amt", 'null') AS DOUBLE) AS intragov_accr_int_pay_mil_amt,
    CAST(NULLIF("intragov_net_unamort_mil_amt", 'null') AS DOUBLE) AS intragov_net_unamort_mil_amt,
    CAST(NULLIF("src_line_nbr", 'null') AS BIGINT) AS src_line_nbr,
    CAST(NULLIF("record_fiscal_year", 'null') AS BIGINT) AS record_fiscal_year,
    CAST(NULLIF("record_fiscal_quarter", 'null') AS BIGINT) AS record_fiscal_quarter,
    CAST(NULLIF("record_calendar_year", 'null') AS BIGINT) AS record_calendar_year,
    CAST(NULLIF("record_calendar_quarter", 'null') AS BIGINT) AS record_calendar_quarter,
    "record_calendar_month",
    "record_calendar_day"
FROM "us-treasury-fiscal-data-v1-accounting-od-schedules-fed-debt-daily-summary"
