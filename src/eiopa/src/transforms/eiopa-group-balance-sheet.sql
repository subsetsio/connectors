SELECT DISTINCT
    reporting_entity,
    reference_period,
    frequency,
    item_code,
    item_name,
    CAST(value AS DOUBLE) AS value,
    TRY_CAST(n_submissions AS BIGINT) AS n_submissions,
    CAST(try_strptime(extraction_date, '%Y%m%d') AS DATE) AS extraction_date
FROM "eiopa-group-balance-sheet"
WHERE value IS NOT NULL
