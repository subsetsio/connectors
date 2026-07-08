SELECT station_id, CAST(t AS DATE) AS date, value AS rainfall_mm FROM "national-river-flow-archive-cdr" WHERE value IS NOT NULL
