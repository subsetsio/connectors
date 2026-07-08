SELECT
    CAST(date AS DATE)      AS date,
    country,
    entity                  AS ide,
    CAST(share AS DOUBLE)   AS share
FROM "pypl-top-ide"
WHERE share IS NOT NULL
