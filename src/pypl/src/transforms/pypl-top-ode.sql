SELECT
    CAST(date AS DATE)      AS date,
    country,
    entity                  AS online_dev_environment,
    CAST(share AS DOUBLE)   AS share
FROM "pypl-top-ode"
WHERE share IS NOT NULL
