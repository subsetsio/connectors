-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Aggregate rows sit alongside the components they sum: `security_class1_desc` ('Grand Total'); `security_class2_desc` ('Total Inflation-Indexed Bonds', 'Total Inflation-Indexed Notes', 'Total Treasury Bonds', …). Summing an amount column without excluding them double-counts.
SELECT
    "record_date",
    "cusip",
    "security_class1_desc",
    "security_class2_desc",
    "interest_rate_pct",
    "maturity_date",
    CAST(NULLIF("outstanding_amt", 'null') AS DOUBLE) AS outstanding_amt,
    CAST(NULLIF("portion_unstripped_amt", 'null') AS DOUBLE) AS portion_unstripped_amt,
    CAST(NULLIF("portion_stripped_amt", 'null') AS BIGINT) AS portion_stripped_amt,
    CAST(NULLIF("reconstituted_amt", 'null') AS BIGINT) AS reconstituted_amt,
    CAST(NULLIF("src_line_nbr", 'null') AS BIGINT) AS src_line_nbr,
    CAST(NULLIF("record_fiscal_year", 'null') AS BIGINT) AS record_fiscal_year,
    CAST(NULLIF("record_fiscal_quarter", 'null') AS BIGINT) AS record_fiscal_quarter,
    CAST(NULLIF("record_calendar_year", 'null') AS BIGINT) AS record_calendar_year,
    CAST(NULLIF("record_calendar_quarter", 'null') AS BIGINT) AS record_calendar_quarter,
    "record_calendar_month",
    CAST(NULLIF("record_calendar_day", 'null') AS BIGINT) AS record_calendar_day
FROM "us-treasury-fiscal-data-v1-debt-mspd-mspd-table-5"
