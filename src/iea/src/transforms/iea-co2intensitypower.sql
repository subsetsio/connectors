SELECT
    CAST("year" AS BIGINT)                        AS year,
    trim(CAST("country" AS VARCHAR), E' \t\n\r')        AS country,
    trim(CAST("short" AS VARCHAR), E' \t\n\r')          AS country_label,
    CAST("value" AS DOUBLE)                       AS value
FROM "iea-co2intensitypower"
WHERE "value" IS NOT NULL
