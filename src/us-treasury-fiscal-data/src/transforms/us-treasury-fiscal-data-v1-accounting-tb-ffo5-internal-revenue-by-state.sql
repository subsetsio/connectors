-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Aggregate rows sit alongside the components they sum: `state_nm` ('United States, total'). Summing an amount column without excluding them double-counts.
SELECT
    "record_date",
    "revenue_fiscal_year",
    "state_nm",
    CAST(NULLIF("total_rev_collect_thous_amt", 'null') AS BIGINT) AS total_rev_collect_thous_amt,
    CAST(NULLIF("business_income_tax_thous_amt", 'null') AS BIGINT) AS business_income_tax_thous_amt,
    CAST(NULLIF("total_indv_tax_thous_amt", 'null') AS BIGINT) AS total_indv_tax_thous_amt,
    CAST(NULLIF("withheld_fica_thous_amt", 'null') AS BIGINT) AS withheld_fica_thous_amt,
    CAST(NULLIF("not_withheld_seca_thous_amt", 'null') AS BIGINT) AS not_withheld_seca_thous_amt,
    CAST(NULLIF("unemployment_ins_tax_thous_amt", 'null') AS BIGINT) AS unemployment_ins_tax_thous_amt,
    CAST(NULLIF("railroad_retire_tax_thous_amt", 'null') AS BIGINT) AS railroad_retire_tax_thous_amt,
    CAST(NULLIF("estate_trust_tax_thous_amt", 'null') AS BIGINT) AS estate_trust_tax_thous_amt,
    CAST(NULLIF("estate_tax_thous_amt", 'null') AS BIGINT) AS estate_tax_thous_amt,
    CAST(NULLIF("gift_tax_thous_amt", 'null') AS BIGINT) AS gift_tax_thous_amt,
    CAST(NULLIF("excise_tax_thous_amt", 'null') AS BIGINT) AS excise_tax_thous_amt,
    CAST(NULLIF("src_line_nbr", 'null') AS BIGINT) AS src_line_nbr,
    CAST(NULLIF("record_fiscal_year", 'null') AS BIGINT) AS record_fiscal_year,
    CAST(NULLIF("record_fiscal_quarter", 'null') AS BIGINT) AS record_fiscal_quarter,
    CAST(NULLIF("record_calendar_year", 'null') AS BIGINT) AS record_calendar_year,
    CAST(NULLIF("record_calendar_quarter", 'null') AS BIGINT) AS record_calendar_quarter,
    CAST(NULLIF("record_calendar_month", 'null') AS BIGINT) AS record_calendar_month,
    "record_calendar_day"
FROM "us-treasury-fiscal-data-v1-accounting-tb-ffo5-internal-revenue-by-state"
