SELECT DISTINCT
    CAST(indicator_id AS BIGINT)   AS indicator_id,
    data_period,
    CAST(year AS INTEGER)          AS year,
    CAST(period_id AS INTEGER)     AS period_id,
    reference_period,
    function_type,
    CAST(value AS DOUBLE)          AS value,
    unit,
    CAST(last_update_date AS TIMESTAMP) AS last_update_date
FROM "dsec-macao-values"
WHERE value IS NOT NULL
  AND year IS NOT NULL
