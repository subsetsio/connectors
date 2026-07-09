SELECT
    alpha3,
    alpha2,
    name,
    continent
FROM "climate-trace-countries"
WHERE alpha3 IS NOT NULL
