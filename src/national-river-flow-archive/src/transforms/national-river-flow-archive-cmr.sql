SELECT station_id, CAST(t || '-01' AS DATE) AS month, value AS rainfall_mm FROM "national-river-flow-archive-cmr" WHERE value IS NOT NULL
