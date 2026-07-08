SELECT
    source, appraisalsource, series, seriesid, frequency, geolevel,
    geoname, statepostal, statefips, fips, purpose,
    CAST(NULLIF(year, '') AS INTEGER)    AS year,
    CAST(NULLIF(quarter, '') AS INTEGER) AS quarter,
    characteristic1, category1, suppressed,
    CAST(NULLIF(value, '') AS DOUBLE)    AS value
FROM "fhfa-uad-aggregate-statistics"
