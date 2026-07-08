SELECT station_id, CAST(t AS DATE) AS date, value AS flow_m3s FROM "national-river-flow-archive-ndf" WHERE value IS NOT NULL
