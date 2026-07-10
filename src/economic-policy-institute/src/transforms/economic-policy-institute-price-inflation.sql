SELECT
    CASE date_interval
        WHEN 'year'    THEN make_date(TRY_CAST(year AS INTEGER), 1, 1)
        WHEN 'quarter' THEN make_date(TRY_CAST(year AS INTEGER),
                                      (TRY_CAST(quarter AS INTEGER) - 1) * 3 + 1, 1)
        WHEN 'month'   THEN make_date(TRY_CAST(year AS INTEGER),
                                      TRY_CAST(month AS INTEGER), 1)
    END                                   AS date,
    date_interval                         AS frequency,
    indicator,
    measure,
    geo_type,
    geo_name,
    geo_code,
    COALESCE(NULLIF("group", ''), 'all') AS group_name,
    COALESCE(NULLIF(group_value, ''), 'all') AS group_value,
    TRY_CAST(value AS DOUBLE)             AS value
FROM "economic-policy-institute-price-inflation"
WHERE TRY_CAST(value AS DOUBLE) IS NOT NULL
  AND TRY_CAST(year AS INTEGER) IS NOT NULL
