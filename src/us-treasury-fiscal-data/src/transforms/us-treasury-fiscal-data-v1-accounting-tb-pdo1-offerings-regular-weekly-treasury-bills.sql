-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "record_date",
    "issue_date",
    "maturity_date",
    CAST(NULLIF("days_to_maturity", 'null') AS BIGINT) AS days_to_maturity,
    CAST(NULLIF("bids_tendered_mil_amt", 'null') AS DOUBLE) AS bids_tendered_mil_amt,
    CAST(NULLIF("bids_acc_total_mil_amt", 'null') AS DOUBLE) AS bids_acc_total_mil_amt,
    CAST(NULLIF("bids_acc_comp_basis_mil_amt", 'null') AS DOUBLE) AS bids_acc_comp_basis_mil_amt,
    CAST(NULLIF("bids_acc_noncomp_basis_mil_amt", 'null') AS DOUBLE) AS bids_acc_noncomp_basis_mil_amt,
    CAST(NULLIF("high_price_per_hundred", 'null') AS DOUBLE) AS high_price_per_hundred,
    CAST(NULLIF("high_discount_rate", 'null') AS DOUBLE) AS high_discount_rate,
    CAST(NULLIF("high_investment_rate", 'null') AS DOUBLE) AS high_investment_rate,
    CAST(NULLIF("src_line_nbr", 'null') AS BIGINT) AS src_line_nbr,
    CAST(NULLIF("record_fiscal_year", 'null') AS BIGINT) AS record_fiscal_year,
    CAST(NULLIF("record_fiscal_quarter", 'null') AS BIGINT) AS record_fiscal_quarter,
    CAST(NULLIF("record_calendar_year", 'null') AS BIGINT) AS record_calendar_year,
    CAST(NULLIF("record_calendar_quarter", 'null') AS BIGINT) AS record_calendar_quarter,
    "record_calendar_month",
    "record_calendar_day"
FROM "us-treasury-fiscal-data-v1-accounting-tb-pdo1-offerings-regular-weekly-treasury-bills"
