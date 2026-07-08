SELECT CAST(year AS INTEGER) AS year, mode,
       CAST(unlinked_passenger_trips_millions AS DOUBLE) AS unlinked_passenger_trips_millions
FROM "american-public-transportation-association-factbook-a-table-1"
WHERE year IS NOT NULL AND mode IS NOT NULL
  AND unlinked_passenger_trips_millions IS NOT NULL
