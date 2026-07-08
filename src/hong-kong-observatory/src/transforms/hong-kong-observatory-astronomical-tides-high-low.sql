SELECT
    station,
    make_date(year, month, day) AS date,
    event,
    time,
    CAST(TRY_CAST(height_m AS DOUBLE) AS DOUBLE) AS height_m
FROM "hong-kong-observatory-astronomical-tides-high-low"
WHERE TRY_CAST(height_m AS DOUBLE) IS NOT NULL
