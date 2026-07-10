-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "record_date",
    "agency_bureau_indicator",
    "agency_nm",
    "bureau_nm",
    "total_eligible_debt_amt",
    "total_eligible_debt_cnt",
    "eligible_debt_referred_amt",
    "eligible_debt_referred_cnt",
    "eligible_debt_not_referred_amt",
    "eligible_debt_not_referred_cnt",
    "compliance_rate_amt",
    "compliance_rate_cnt",
    "cfo_agency_indicator",
    CAST(NULLIF("record_fiscal_year", 'null') AS BIGINT) AS record_fiscal_year,
    CAST(NULLIF("record_fiscal_quarter", 'null') AS BIGINT) AS record_fiscal_quarter,
    CAST(NULLIF("record_calendar_year", 'null') AS BIGINT) AS record_calendar_year,
    CAST(NULLIF("record_calendar_quarter", 'null') AS BIGINT) AS record_calendar_quarter,
    "record_calendar_month",
    CAST(NULLIF("record_calendar_day", 'null') AS BIGINT) AS record_calendar_day
FROM "us-treasury-fiscal-data-v2-debt-tror-data-act-compliance"
