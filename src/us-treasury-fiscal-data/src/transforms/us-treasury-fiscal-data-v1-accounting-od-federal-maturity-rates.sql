-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "record_date",
    CAST(NULLIF("record_fiscal_year", 'null') AS BIGINT) AS record_fiscal_year,
    CAST(NULLIF("one_year_or_less", 'null') AS DOUBLE) AS one_year_or_less,
    CAST(NULLIF("between_1_and_5_years", 'null') AS DOUBLE) AS between_1_and_5_years,
    CAST(NULLIF("between_5_and_10_years", 'null') AS DOUBLE) AS between_5_and_10_years,
    CAST(NULLIF("between_10_and_20_years", 'null') AS DOUBLE) AS between_10_and_20_years,
    CAST(NULLIF("twenty_years_or_greater", 'null') AS DOUBLE) AS twenty_years_or_greater,
    CAST(NULLIF("src_line_nbr", 'null') AS BIGINT) AS src_line_nbr,
    CAST(NULLIF("record_fiscal_quarter", 'null') AS BIGINT) AS record_fiscal_quarter,
    CAST(NULLIF("record_calendar_year", 'null') AS BIGINT) AS record_calendar_year,
    CAST(NULLIF("record_calendar_quarter", 'null') AS BIGINT) AS record_calendar_quarter,
    "record_calendar_month",
    CAST(NULLIF("record_calendar_day", 'null') AS BIGINT) AS record_calendar_day
FROM "us-treasury-fiscal-data-v1-accounting-od-federal-maturity-rates"
