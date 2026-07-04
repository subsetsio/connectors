SELECT
    CAST("year" AS BIGINT)                        AS year,
    trim(CAST("country" AS VARCHAR), E' \t\n\r')        AS country,
    trim(CAST("short" AS VARCHAR), E' \t\n\r')          AS country_label,
    trim(CAST("flow" AS VARCHAR), E' \t\n\r')           AS flow,
    trim(CAST("flowLabel" AS VARCHAR), E' \t\n\r')      AS flow_label,
    CAST("value" AS DOUBLE)                       AS value
FROM "iea-elecimportsexports"
WHERE "value" IS NOT NULL
