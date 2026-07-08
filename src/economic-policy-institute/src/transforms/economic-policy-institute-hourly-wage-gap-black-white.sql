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
    NULLIF("group", '')                   AS group_name,
    group_value,
    TRY_CAST(value AS DOUBLE)             AS value
FROM "economic-policy-institute-hourly-wage-gap-black-white"
WHERE TRY_CAST(value AS DOUBLE) IS NOT NULL
  AND TRY_CAST(year AS INTEGER) IS NOT NULL
