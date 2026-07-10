-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "fed_act_statement",
    "eff_date",
    CAST(NULLIF("shares_per_par", 'null') AS DOUBLE) AS shares_per_par,
    "trans_desc_cd",
    CAST(NULLIF("memo_nbr", 'null') AS BIGINT) AS memo_nbr,
    "location_cd",
    "acct_desc",
    "acct_nbr",
    CAST(NULLIF("record_fiscal_year", 'null') AS BIGINT) AS record_fiscal_year,
    CAST(NULLIF("record_fiscal_quarter", 'null') AS BIGINT) AS record_fiscal_quarter,
    CAST(NULLIF("record_calendar_year", 'null') AS BIGINT) AS record_calendar_year,
    CAST(NULLIF("record_calendar_quarter", 'null') AS BIGINT) AS record_calendar_quarter,
    "record_calendar_month",
    "record_calendar_day"
FROM "us-treasury-fiscal-data-v1-accounting-od-utf-federal-activity-statement"
