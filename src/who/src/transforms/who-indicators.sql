SELECT
    IndicatorCode AS indicator_code,
    IndicatorName AS indicator_name,
    Language      AS language
FROM "who-indicators"
WHERE IndicatorCode IS NOT NULL
