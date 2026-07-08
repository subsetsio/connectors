SELECT
    CAST(year AS INTEGER) AS year,
    TRY_CAST(teus_in_million AS DOUBLE) AS teus_in_million
FROM "port-of-la-38a8-tm7u"
WHERE year IS NOT NULL
