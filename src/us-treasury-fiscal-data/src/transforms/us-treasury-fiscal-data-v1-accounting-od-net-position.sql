-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Aggregate rows sit alongside the components they sum: `line_item_desc` ('Total net cost', 'Total revenue'). Summing an amount column without excluding them double-counts.
-- caution: One `record_date` carries many `stmt_fiscal_year` rows — `stmt_fiscal_year` is part of the row identity, because each publication restates a whole block of years. Filter or group by `stmt_fiscal_year` before aggregating.
SELECT
    "record_date",
    CAST(NULLIF("stmt_fiscal_year", 'null') AS BIGINT) AS stmt_fiscal_year,
    "restmt_flag",
    "account_desc",
    "line_item_desc",
    "non_dedicated_funds_bil_amt",
    "dedicated_funds_bil_amt",
    "eliminations_bil_amt",
    "consolidated_bil_amt",
    CAST(NULLIF("src_line_nbr", 'null') AS BIGINT) AS src_line_nbr,
    CAST(NULLIF("record_fiscal_year", 'null') AS BIGINT) AS record_fiscal_year,
    CAST(NULLIF("record_fiscal_quarter", 'null') AS BIGINT) AS record_fiscal_quarter,
    CAST(NULLIF("record_calendar_year", 'null') AS BIGINT) AS record_calendar_year,
    CAST(NULLIF("record_calendar_quarter", 'null') AS BIGINT) AS record_calendar_quarter,
    "record_calendar_month",
    CAST(NULLIF("record_calendar_day", 'null') AS BIGINT) AS record_calendar_day
FROM "us-treasury-fiscal-data-v1-accounting-od-net-position"
