SELECT
    CAST(year AS INTEGER) AS year,
    TRY_CAST(ship_calls AS INTEGER) AS ship_calls,
    TRY_CAST(passengers AS BIGINT) AS passengers,
    TRY_CAST(passengers_per_ship AS INTEGER) AS passengers_per_ship
FROM "port-of-la-jmt8-y5rm"
WHERE year IS NOT NULL
