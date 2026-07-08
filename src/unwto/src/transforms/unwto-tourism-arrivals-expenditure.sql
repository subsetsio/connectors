SELECT
    country_code,
    max(country) AS country,
    year,
    max(value) FILTER (WHERE series = 'arrivals')           AS arrivals_thousands,
    max(arrivals_type) FILTER (WHERE series = 'arrivals')   AS arrivals_type,
    max(value) FILTER (WHERE series = 'expenditure')        AS expenditure_millions_usd
FROM "unwto-tourism-arrivals-expenditure"
GROUP BY country_code, year
