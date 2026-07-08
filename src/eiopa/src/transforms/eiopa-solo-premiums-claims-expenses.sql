SELECT DISTINCT
    reporting_entity,
    reference_period,
    frequency,
    metric,
    business_type,
    item_code,
    CAST(value AS DOUBLE) AS value,
    TRY_CAST(n_submissions AS BIGINT) AS n_submissions,
    CAST(try_strptime(extraction_date, '%Y%m%d') AS DATE) AS extraction_date
FROM "eiopa-solo-premiums-claims-expenses"
WHERE value IS NOT NULL
