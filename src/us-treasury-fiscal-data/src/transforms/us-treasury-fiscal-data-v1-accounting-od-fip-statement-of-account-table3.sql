-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Aggregate rows sit alongside the components they sum: `sub_category` ('GRAND TOTALS', 'TRANSACTION DETAIL TOTALS'). Summing an amount column without excluding them double-counts.
SELECT
    "record_date",
    "account_number_tas",
    "account_name",
    "date_range",
    "trans_date",
    "memo_no",
    "sub_category",
    CAST(NULLIF("principal_inflation_comp", 'null') AS DOUBLE) AS principal_inflation_comp,
    CAST(NULLIF("unrealized_discount", 'null') AS DOUBLE) AS unrealized_discount,
    CAST(NULLIF("premium_discount_recognized", 'null') AS DOUBLE) AS premium_discount_recognized,
    CAST(NULLIF("interest_inflation_earnings", 'null') AS DOUBLE) AS interest_inflation_earnings,
    CAST(NULLIF("total_investments", 'null') AS DOUBLE) AS total_investments,
    CAST(NULLIF("total_redemptions", 'null') AS DOUBLE) AS total_redemptions,
    CAST(NULLIF("total_inflation_purchased_sold", 'null') AS DOUBLE) AS total_inflation_purchased_sold,
    CAST(NULLIF("src_line_nbr", 'null') AS BIGINT) AS src_line_nbr,
    CAST(NULLIF("record_fiscal_year", 'null') AS BIGINT) AS record_fiscal_year,
    CAST(NULLIF("record_fiscal_quarter", 'null') AS BIGINT) AS record_fiscal_quarter,
    CAST(NULLIF("record_calendar_year", 'null') AS BIGINT) AS record_calendar_year,
    CAST(NULLIF("record_calendar_quarter", 'null') AS BIGINT) AS record_calendar_quarter,
    "record_calendar_month",
    "record_calendar_day"
FROM "us-treasury-fiscal-data-v1-accounting-od-fip-statement-of-account-table3"
