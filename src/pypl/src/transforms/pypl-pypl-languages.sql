SELECT
    CAST(date AS DATE)      AS date,
    country,
    entity                  AS language,
    CAST(share AS DOUBLE)   AS share
FROM "pypl-pypl-languages"
WHERE share IS NOT NULL
