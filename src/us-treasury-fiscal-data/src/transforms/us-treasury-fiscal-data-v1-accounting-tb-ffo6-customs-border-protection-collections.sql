-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Aggregate rows sit alongside the components they sum: `port_cd` ('Total'); `port_nm` ('Total'). Summing an amount column without excluding them double-counts.
-- caution: One `record_date` carries many `collection_fiscal_year` rows — `collection_fiscal_year` is part of the row identity, because each publication restates a whole block of years. Filter or group by `collection_fiscal_year` before aggregating.
SELECT
    "record_date",
    "collection_fiscal_year",
    "district_nm",
    "port_nm",
    "port_cd",
    CAST(NULLIF("collection_amt", 'null') AS DOUBLE) AS collection_amt,
    CAST(NULLIF("src_line_nbr", 'null') AS BIGINT) AS src_line_nbr,
    CAST(NULLIF("record_fiscal_year", 'null') AS BIGINT) AS record_fiscal_year,
    CAST(NULLIF("record_fiscal_quarter", 'null') AS BIGINT) AS record_fiscal_quarter,
    CAST(NULLIF("record_calendar_year", 'null') AS BIGINT) AS record_calendar_year,
    CAST(NULLIF("record_calendar_quarter", 'null') AS BIGINT) AS record_calendar_quarter,
    CAST(NULLIF("record_calendar_month", 'null') AS BIGINT) AS record_calendar_month,
    "record_calendar_day"
FROM "us-treasury-fiscal-data-v1-accounting-tb-ffo6-customs-border-protection-collections"
