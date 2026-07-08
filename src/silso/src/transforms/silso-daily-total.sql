SELECT
    make_date(year, month, day)        AS date,
    NULLIF(sunspot_number, -1)         AS sunspot_number,
    NULLIF(std_dev, -1)                AS std_dev,
    NULLIF(n_observations, -1)         AS n_observations,
    definitive = 1                     AS definitive
FROM "silso-daily-total"
WHERE NULLIF(sunspot_number, -1) IS NOT NULL
