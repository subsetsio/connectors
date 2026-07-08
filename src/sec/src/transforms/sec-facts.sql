SELECT
    CAST(cik AS BIGINT)        AS cik,
    entity_name,
    taxonomy,
    tag,
    unit,
    CAST(fiscal_year AS INTEGER) AS fiscal_year,
    fiscal_period,
    TRY_CAST(period_start AS DATE) AS period_start,
    CAST(period_end AS DATE)       AS period_end,
    CAST(value AS DOUBLE)          AS value,
    accession,
    loc
FROM "sec-facts"
WHERE value IS NOT NULL
  AND cik IS NOT NULL
  AND period_end IS NOT NULL
