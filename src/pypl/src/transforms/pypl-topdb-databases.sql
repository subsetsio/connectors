SELECT
    CAST(date AS DATE)      AS date,
    country,
    entity                  AS database,
    CAST(share AS DOUBLE)   AS share
FROM "pypl-topdb-databases"
WHERE share IS NOT NULL
