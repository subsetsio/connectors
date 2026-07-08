SELECT
    source, frequency, geolevel, geoid, geoname, market, period,
    CAST(NULLIF(year, '') AS INTEGER)     AS year,
    CAST(NULLIF(quarter, '') AS INTEGER)  AS quarter,
    CAST(NULLIF(month, '') AS INTEGER)    AS month,
    suppressed, seriesid,
    CAST(NULLIF(value1, '') AS DOUBLE)    AS value1,
    CAST(NULLIF(value2, '') AS DOUBLE)    AS value2
FROM "fhfa-nmdb-aggregate-statistics"
