SELECT station_id, CAST(t || '-01' AS DATE) AS month, value AS flow_m3s FROM "national-river-flow-archive-gmf" WHERE value IS NOT NULL
