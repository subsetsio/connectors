SELECT
    statistic_code,
    table_code,
    table_name,
    "time"            AS time_label,
    measure_code,
    dims              AS dimensions,
    CAST(value AS DOUBLE) AS value,
    status
FROM "destatis-46241"
WHERE value IS NOT NULL
