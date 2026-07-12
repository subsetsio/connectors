SELECT
    CAST(date AS DATE) AS date,
    CAST(n10d AS DOUBLE) AS n10d,
    CAST(gprd AS DOUBLE) AS gprd,
    CAST(gprd_act AS DOUBLE) AS gprd_act,
    CAST(gprd_threat AS DOUBLE) AS gprd_threat,
    CAST(gprd_ma30 AS DOUBLE) AS gprd_ma30,
    CAST(gprd_ma7 AS DOUBLE) AS gprd_ma7,
    CAST(event AS VARCHAR) AS event
FROM "geopolitical-risk-index-gpr-daily"
WHERE gprd IS NOT NULL
