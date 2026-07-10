-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "record_date",
    "electronic_category_desc",
    "channel_type_desc",
    "tax_category_desc",
    CAST(NULLIF("net_collections_amt", 'null') AS DOUBLE) AS net_collections_amt,
    CAST(NULLIF("electronic_category_id", 'null') AS BIGINT) AS electronic_category_id,
    CAST(NULLIF("channel_type_id", 'null') AS BIGINT) AS channel_type_id,
    CAST(NULLIF("tax_category_id", 'null') AS BIGINT) AS tax_category_id,
    CAST(NULLIF("src_line_nbr", 'null') AS BIGINT) AS src_line_nbr,
    CAST(NULLIF("record_fiscal_year", 'null') AS BIGINT) AS record_fiscal_year,
    CAST(NULLIF("record_fiscal_quarter", 'null') AS BIGINT) AS record_fiscal_quarter,
    CAST(NULLIF("record_calendar_year", 'null') AS BIGINT) AS record_calendar_year,
    CAST(NULLIF("record_calendar_quarter", 'null') AS BIGINT) AS record_calendar_quarter,
    "record_calendar_month",
    "record_calendar_day"
FROM "us-treasury-fiscal-data-v2-revenue-rcm"
