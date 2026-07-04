SELECT
    CAST("year" AS BIGINT)                        AS year,
    trim(CAST("country" AS VARCHAR), E' \t\n\r')        AS country,
    trim(CAST("short" AS VARCHAR), E' \t\n\r')          AS country_label,
    trim(CAST("product" AS VARCHAR), E' \t\n\r')           AS product,
    trim(CAST("productLabel" AS VARCHAR), E' \t\n\r')      AS product_label,
    CAST("value" AS DOUBLE)                       AS value
FROM "iea-wasteheatbysource"
WHERE "value" IS NOT NULL
