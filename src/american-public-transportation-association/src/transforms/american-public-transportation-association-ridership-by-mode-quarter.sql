SELECT CAST(year AS INTEGER) AS year, quarter,
       CAST(total_unlinked_trips_000s AS DOUBLE) AS total_unlinked_trips_000s,
       CAST(heavy_rail_000s AS DOUBLE) AS heavy_rail_000s,
       CAST(light_rail_000s AS DOUBLE) AS light_rail_000s,
       CAST(commuter_rail_000s AS DOUBLE) AS commuter_rail_000s,
       CAST(trolleybus_000s AS DOUBLE) AS trolleybus_000s,
       CAST(bus_000s AS DOUBLE) AS bus_000s,
       CAST(demand_response_000s AS DOUBLE) AS demand_response_000s,
       CAST(other_000s AS DOUBLE) AS other_000s
FROM "american-public-transportation-association-ridership-by-mode-quarter"
WHERE year IS NOT NULL AND quarter IS NOT NULL
