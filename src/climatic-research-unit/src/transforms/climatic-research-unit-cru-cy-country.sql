SELECT
    country,
    variable,
    unit,
    make_date(year, month, 1) AS date,
    year,
    month,
    CAST(value AS DOUBLE) AS value
FROM "climatic-research-unit-cru-cy-country"
WHERE value IS NOT NULL
